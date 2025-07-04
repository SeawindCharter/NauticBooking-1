# NauticBooking - Sistema de Gestión de Reservas Náuticas

## Overview

NauticBooking is a Flask-based web application for managing nautical reservations. It provides a comprehensive system for boat rental management, including customer information, booking details, payment tracking, and promotional codes. The application features both public and admin interfaces, with Excel import capabilities and comprehensive reporting features.

## System Architecture

### Frontend Architecture
- **Framework**: Flask with Jinja2 templating
- **UI Framework**: Bootstrap 5 with dark theme
- **Styling**: Custom CSS with FontAwesome icons
- **JavaScript**: Vanilla JavaScript for form validation and UI enhancements
- **Responsive Design**: Mobile-first approach using Bootstrap grid system

### Backend Architecture
- **Framework**: Flask web framework
- **Database ORM**: SQLAlchemy with declarative base
- **Authentication**: Flask-Login for session management
- **Form Handling**: Flask-WTF with WTForms for validation
- **File Upload**: Werkzeug for secure file handling
- **Password Security**: Werkzeug security utilities for hashing

### Data Storage
- **Primary Database**: SQLite (development) / PostgreSQL (production ready)
- **Session Management**: Flask sessions with secret key
- **File Storage**: Local filesystem for Excel uploads
- **Connection Pooling**: SQLAlchemy engine with pool recycling

## Key Components

### Models
- **Admin**: User management with authentication
- **Reserva**: Core booking entity with customer and boat information
- **CodigoPromocional**: Promotional code system for discounts

### Main Features
- **Reservation Management**: Create, edit, view, and search reservations
- **Customer Tracking**: Store customer contact information and booking history
- **Payment Tracking**: Multiple payment phases (Pago A, Pago B) with balance calculation
- **Boat Fleet Management**: Predefined boat types with selection system
- **Promotional Codes**: Discount system with validation
- **Excel Import**: Bulk reservation import from spreadsheets
- **Admin Dashboard**: Statistics and management interface

### Security Features
- **Authentication**: Login-required admin sections
- **Password Hashing**: Secure password storage
- **Session Management**: Remember me functionality
- **File Validation**: Secure file upload with type checking
- **Form Validation**: Server-side and client-side validation

## Data Flow

1. **Public Interface**: 
   - Users can view reservation statistics on homepage
   - Public access to reservation listing and creation

2. **Admin Interface**:
   - Secure login system for administrative access
   - Dashboard with comprehensive statistics
   - Excel import functionality for bulk operations
   - Advanced reporting capabilities

3. **Reservation Process**:
   - Form-based reservation creation with validation
   - Automatic calculation of booking duration and balances
   - Promotional code validation and discount application
   - Payment tracking with multiple installment support

4. **Data Persistence**:
   - SQLAlchemy ORM handles all database operations
   - Automatic timestamp tracking for auditing
   - Relationship management between entities

## External Dependencies

### Python Packages
- **Flask**: Web framework and core functionality
- **Flask-SQLAlchemy**: Database ORM integration
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and CSRF protection
- **Pandas**: Excel file processing and data manipulation
- **Werkzeug**: Security utilities and file handling

### Frontend Dependencies
- **Bootstrap 5**: UI framework with dark theme
- **FontAwesome**: Icon library
- **Custom CSS**: Application-specific styling

### Infrastructure
- **ProxyFix**: Middleware for reverse proxy support
- **File System**: Local storage for uploads
- **Environment Variables**: Configuration management

## Deployment Strategy

### Development Setup
- SQLite database for local development
- Debug mode enabled for development
- Local file storage for uploads
- Environment-based configuration

### Production Considerations
- PostgreSQL database recommended for production
- Environment variable configuration for sensitive data
- Secure file upload directory with proper permissions
- Session secret key management
- Reverse proxy support configured

### Configuration Management
- Environment variables for database URLs
- Upload folder configuration
- Session secret key externalization
- Debug mode control

## Changelog
- July 03, 2025. Initial setup
- July 04, 2025. Fixed reservation editing functionality completely
- July 04, 2025. Created unique admin profile: Santiago/Santiago123
- July 04, 2025. Fixed timestamp updates for reservation modifications

## User Preferences

Preferred communication style: Simple, everyday language.

## Technical Notes

### Admin Credentials
- Username: Santiago
- Password: Santiago123
- Email: santiago@nauticbooking.com

### System Status
- Database: ✅ Fully functional
- Edit functionality: ✅ Working correctly
- Timestamp updates: ✅ Working correctly
- Frontend-backend connection: ✅ Verified working