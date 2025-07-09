from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
import secrets

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost/jobs_for_teens')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    listings = db.relationship('BusinessListing', backref='owner', lazy=True)
    verifications = db.relationship('ListingVerification', backref='user', lazy=True)

    def set_password(self, password):
        # self.password_hash = generate_password_hash(password)
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class BusinessListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    business_name = db.Column(db.String(120), nullable=False)
    street1 = db.Column(db.String(120), nullable=False)
    street2 = db.Column(db.String(120))
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20))
    business_type = db.Column(db.String(50), nullable=False)
    fulltime_min_age = db.Column(db.Integer)
    parttime_min_age = db.Column(db.Integer)
    verified = db.Column(db.Boolean, default=False)
    verifications = db.relationship('ListingVerification', backref='listing', lazy=True)

class ListingVerification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('business_listing.id'), nullable=False)
    thumbs_up = db.Column(db.Boolean, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(32), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'error': 'Email already exists'}), 400
    
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    print("You have called me... with data: ", data)
    user = User.query.filter_by(email=data['email']).first()
    print(user)
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/reset-password/request', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
        
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'If an account exists with this email, you will receive a password reset link'}), 200
        
    # Generate reset token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    # Delete any existing tokens for this user
    PasswordResetToken.query.filter_by(user_id=user.id).delete()
    
    # Create new token
    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expires_at
    )
    db.session.add(reset_token)
    db.session.commit()
    
    # Send email
    reset_url = f"http://localhost:5173/reset-password/{token}"
    msg = Message(
        'Password Reset Request',
        recipients=[email],
        body=f"To reset your password, click this link: {reset_url}. This link will expire in 24 hours."
    )
    mail.send(msg)
    
    return jsonify({'message': 'If an account exists with this email, you will receive a password reset link'}), 200

@app.route('/api/reset-password/<token>', methods=['POST'])
def reset_password(token):
    reset_token = PasswordResetToken.query.filter_by(token=token, used=False).first()
    
    if not reset_token:
        return jsonify({'error': 'Invalid or expired reset token'}), 400
        
    if reset_token.expires_at < datetime.utcnow():
        return jsonify({'error': 'Reset token has expired'}), 400
        
    data = request.get_json()
    new_password = data.get('password')
    
    if not new_password:
        return jsonify({'error': 'New password is required'}), 400
        
    user = User.query.get(reset_token.user_id)
    user.set_password(new_password)
    
    # Mark token as used
    reset_token.used = True
    db.session.commit()
    
    return jsonify({'message': 'Password has been reset successfully'}), 200

@app.route('/api/businesses', methods=['GET'])
def search_businesses():
    city = request.args.get('city')
    state = request.args.get('state')
    zip_code = request.args.get('zip')
    min_age = request.args.get('min_age', type=int)
    
    query = BusinessListing.query
    
    if city:
        query = query.filter(BusinessListing.city.ilike(f'%{city}%'))
    if state:
        query = query.filter(BusinessListing.state == state)
    if zip_code:
        query = query.filter(BusinessListing.zip_code == zip_code)
    if min_age:
        query = query.filter(
            (BusinessListing.fulltime_min_age <= min_age) | 
            (BusinessListing.parttime_min_age <= min_age)
        )
    
    listings = query.all()
    return jsonify([{
        'id': listing.id,
        'business_name': listing.business_name,
        'address': f"{listing.street1}, {listing.street2 or ''}, {listing.city}, {listing.state} {listing.zip_code}",
        'phone': listing.phone,
        'business_type': listing.business_type,
        'fulltime_min_age': listing.fulltime_min_age,
        'parttime_min_age': listing.parttime_min_age,
        'verified': listing.verified
    } for listing in listings])

@app.route('/api/businesses', methods=['POST'])
@login_required
def add_business():
    data = request.get_json()
    new_listing = BusinessListing(
        owner_id=current_user.id,
        business_name=data['business_name'],
        street1=data['street1'],
        street2=data.get('street2', ''),
        city=data['city'],
        state=data['state'],
        zip_code=data['zip_code'],
        phone=data['phone'],
        business_type=data['business_type'],
        fulltime_min_age=data['fulltime_min_age'],
        parttime_min_age=data['parttime_min_age']
    )
    db.session.add(new_listing)
    db.session.commit()
    return jsonify({'message': 'Business added successfully'}), 201

@app.route('/api/businesses/<int:id>', methods=['PUT'])
@login_required
def update_business(id):
    listing = BusinessListing.query.get_or_404(id)
    if listing.owner_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    for key, value in data.items():
        setattr(listing, key, value)
    
    db.session.commit()
    return jsonify({'message': 'Business updated successfully'}), 200

@app.route('/api/businesses/<int:id>/verify', methods=['POST'])
@login_required
def verify_business(id):
    listing = BusinessListing.query.get_or_404(id)
    data = request.get_json()
    
    verification = ListingVerification(
        user_id=current_user.id,
        listing_id=id,
        thumbs_up=data['thumbs_up'],
        comment=data.get('comment', '')
    )
    
    db.session.add(verification)
    
    # Update verified status based on thumbs up/down ratio
    thumbs_up = ListingVerification.query.filter_by(
        listing_id=id,
        thumbs_up=True
    ).count()
    thumbs_down = ListingVerification.query.filter_by(
        listing_id=id,
        thumbs_up=False
    ).count()
    
    listing.verified = thumbs_up > thumbs_down
    db.session.commit()
    
    return jsonify({'message': 'Verification submitted successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0",debug=True, port=8000)
