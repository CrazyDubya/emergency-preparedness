# Emergency Preparedness System v3.0 - Enhanced Edition

## 🚨 Complete Disaster Readiness Platform

A comprehensive emergency preparedness system with **stateful operations**, **CLI interface**, **REST API**, and **web GUI**. Now with persistent user profiles, automatic backups, and multi-interface access.

## ✨ New Features in v3.0

### 🔄 Stateful Operations
- **Persistent User Profiles** - Never re-enter family/location data
- **Intelligent Caching** - Risk assessments cached for 30 days
- **Smart Updates** - Only asks for information when needed
- **Activity Tracking** - Complete history of all actions

### 💻 CLI with Arguments
```bash
# Interactive mode
python integrated_preparedness_system.py

# Direct commands
python integrated_preparedness_system.py --risk-assessment --output results.json
python integrated_preparedness_system.py --supplies --check-expiry  
python integrated_preparedness_system.py --drill earthquake
python integrated_preparedness_system.py --backup
python integrated_preparedness_system.py --status
```

### 🌐 REST API Server
- **FastAPI** with automatic documentation
- **API Key Authentication** with role-based access
- **Real-time WebSocket** updates
- **CORS Support** for web interfaces
- **Complete CRUD** operations for all data

### 🖥️ Web GUI Interface
- **Streamlit-based** user-friendly interface
- **Real-time Dashboard** with charts and metrics
- **Drag-and-drop** supply management
- **Interactive Drill** simulations
- **Automatic API fallback** to direct system access

### 💾 Comprehensive Backup System
- **Automatic Backups** with configurable intervals
- **Versioned Storage** (keeps last 10 backups)
- **Integrity Verification** with checksum validation
- **Compressed Archives** for efficient storage
- **Easy Restore** from any backup point

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_enhanced.txt
```

### 2. Run in Different Modes

**Interactive CLI Mode:**
```bash
python integrated_preparedness_system.py
```

**Direct CLI Commands:**
```bash
python integrated_preparedness_system.py --status
python integrated_preparedness_system.py --risk-assessment
python integrated_preparedness_system.py --backup
```

**API Server:**
```bash
python api_server.py
# Visit http://localhost:8000/docs for API documentation
```

**Web GUI:**
```bash
streamlit run streamlit_gui.py
# Visit http://localhost:8501
```

## 📖 Usage Examples

### CLI Usage
```bash
# Check system status
python integrated_preparedness_system.py --status

# Run risk assessment with output
python integrated_preparedness_system.py --risk-assessment --output my_risk.json

# Check supply expiry dates  
python integrated_preparedness_system.py --supplies --check-expiry

# Run emergency drill
python integrated_preparedness_system.py --drill earthquake

# Create backup
python integrated_preparedness_system.py --backup

# Export data as JSON
python integrated_preparedness_system.py --export json

# Use specific profile
python integrated_preparedness_system.py --profile family --risk-assessment
```

### API Usage
```bash
# Login and get token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "user_key"}'

# Get profile information
curl -X GET "http://localhost:8000/api/profile" \
  -H "Authorization: Bearer user_key"

# Calculate risk
curl -X POST "http://localhost:8000/api/risk/calculate" \
  -H "Authorization: Bearer user_key" \
  -H "Content-Type: application/json" \
  -d '{"scenario_type": "earthquake", "severity": 7, "location": "suburban"}'

# Start drill
curl -X POST "http://localhost:8000/api/drills/start" \
  -H "Authorization: Bearer user_key" \
  -H "Content-Type: application/json" \
  -d '{"drill_type": "fire", "participants": 4}'

# Create backup
curl -X POST "http://localhost:8000/api/backup/create" \
  -H "Authorization: Bearer user_key" \
  -H "Content-Type: application/json" \
  -d '{"description": "Manual backup via API"}'
```

## 🏗️ Architecture

### System Components
```
Enhanced Emergency Preparedness System v3.0
├── Core System (integrated_preparedness_system.py)
│   ├── 43 Menu Options (All Phase 3 features)
│   ├── Stateful Profile Manager
│   └── Automatic Backup System
├── CLI Interface (argparse-based)
│   ├── Direct Command Execution
│   ├── Batch Processing
│   └── Output Format Options
├── REST API (api_server.py)
│   ├── FastAPI with Auto-docs
│   ├── JWT Authentication
│   ├── WebSocket Support
│   └── CORS for Web GUI
├── Web GUI (streamlit_gui.py)
│   ├── Interactive Dashboard
│   ├── Real-time Charts
│   ├── API Integration
│   └── Direct System Fallback
└── Data Management
    ├── User Profile Manager
    ├── Backup Manager
    ├── 21 SQLite Databases
    └── Profile/Cache Storage
```

### File Structure
```
claude-disaster/
├── integrated_preparedness_system.py    # Enhanced main system
├── user_profile_manager.py              # Stateful profile management
├── backup_manager.py                    # Comprehensive backups
├── api_server.py                        # FastAPI REST server
├── streamlit_gui.py                     # Web GUI interface
├── requirements_enhanced.txt            # All dependencies
├── v2_modules/                          # Phase 3 modules (29 modules)
├── preparedness_data/                   # Data directory
│   ├── profiles/                        # User profiles
│   ├── backups/                         # Versioned backups
│   └── *.db                            # SQLite databases (21 files)
└── README_ENHANCED.md                   # This file
```

## 🔑 API Authentication

The system uses API keys for authentication:

- **admin_key** - Full administrative access
- **user_key** - Standard user access  
- **gui_key** - Embedded in web GUI

### Default API Keys (Change in Production!)
```python
api_keys = {
    "admin_key": {"user_id": "admin", "role": "admin", "profile": "admin"},
    "user_key": {"user_id": "user1", "role": "user", "profile": "default"},
    "gui_key": {"user_id": "gui", "role": "user", "profile": "default"}
}
```

## 📊 API Endpoints

### Authentication
- `POST /auth/login` - Login with API key

### Profile Management  
- `GET /api/profile` - Get current profile
- `PUT /api/profile` - Update profile sections

### Risk Assessment
- `GET /api/risk/assessment` - Get cached assessment
- `POST /api/risk/calculate` - Calculate new risk

### Supply Management
- `GET /api/supplies/inventory` - Get inventory
- `GET /api/supplies/expiry` - Check expiring items

### Alerts & Monitoring
- `GET /api/alerts/active` - Get active alerts
- `POST /api/alerts/subscribe` - Subscribe to alerts

### Training & Drills  
- `POST /api/drills/start` - Start emergency drill
- `GET /api/drills/history` - Get drill history

### Backup & Export
- `POST /api/backup/create` - Create backup
- `GET /api/backup/list` - List backups
- `GET /api/export/{format}` - Export data

### Reports
- `GET /api/reports/comprehensive` - Generate full report

## 🎯 Profile Management

### Automatic Caching
The system intelligently caches data with different expiry periods:

- **Risk Assessment**: 30 days
- **Family Info**: 180 days (6 months)  
- **Location**: 365 days (1 year)
- **Contacts**: 90 days (3 months)
- **Supplies**: 7 days (1 week)
- **Drills**: 14 days (2 weeks)

### Profile Structure
```json
{
  "meta": {
    "version": "1.0",
    "created": "2025-08-13T22:56:54.019106",
    "profile_id": "abc123def456"
  },
  "family": {
    "adults": 2,
    "children": 1,
    "pets": 1,
    "last_updated": "2025-08-13T22:56:54.019128"
  },
  "location": {
    "type": "suburban",
    "housing": "house", 
    "ownership": "own",
    "last_updated": "2025-08-13T22:56:54.019128"
  },
  "risk_assessment": {
    "top_risks": [...],
    "preparedness_score": 75,
    "last_updated": "2025-08-13T22:56:54.019128"
  }
}
```

## 💾 Backup System

### Automatic Backups
- **Frequency**: Every 24 hours by default
- **Retention**: Keeps last 10 backups
- **Compression**: ZIP format for efficiency
- **Verification**: Integrity checking with checksums

### Backup Contents
- All SQLite databases (21 files)
- User profiles and preferences
- Configuration files
- Activity history

### Manual Backup
```bash
# CLI
python integrated_preparedness_system.py --backup

# API
curl -X POST "http://localhost:8000/api/backup/create" \
  -H "Authorization: Bearer user_key"

# GUI
# Use the Backup & Export page
```

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration
export API_SECRET_KEY="your-secret-key-here"
export API_HOST="0.0.0.0"
export API_PORT="8000"

# Database Configuration  
export DATA_DIR="preparedness_data"
export BACKUP_RETENTION="10"
export AUTO_BACKUP_HOURS="24"

# GUI Configuration
export STREAMLIT_SERVER_PORT="8501"
export STREAMLIT_SERVER_ADDRESS="0.0.0.0"
```

### Custom Profiles
```bash
# Create new profile
python integrated_preparedness_system.py --profile family

# List profiles
python integrated_preparedness_system.py --list-profiles

# Switch profiles
python integrated_preparedness_system.py --profile work --status
```

## 📈 Performance & Scaling

### Resource Usage
- **Memory**: 50-100MB typical usage
- **Storage**: ~500MB for full dataset
- **CPU**: Low usage, spikes during risk calculations

### Scaling Considerations
- **Multi-user**: API supports multiple concurrent users
- **Database**: SQLite suitable for single-server deployment
- **Caching**: Intelligent caching reduces computational load
- **Backups**: Compressed backups minimize storage

## 🔒 Security

### API Security
- **API Key Authentication** with role-based access
- **CORS Configuration** for web security
- **Request Rate Limiting** (planned)
- **Input Validation** with Pydantic models

### Data Security
- **Local Storage** - All data stays on your system
- **Backup Encryption** (planned)
- **Access Logging** for audit trails
- **Profile Isolation** between users

## 🚨 Troubleshooting

### Common Issues

**"No module named 'v2_modules'"**
```bash
# Ensure you're in the correct directory
cd /path/to/claude-disaster
python integrated_preparedness_system.py
```

**API Server Won't Start**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Use different port
uvicorn api_server:app --port 8001
```

**GUI Can't Connect to API**
```bash
# Start API server first
python api_server.py

# Then start GUI
streamlit run streamlit_gui.py
```

**Profile Data Missing**
```bash
# Check profile directory
ls preparedness_data/profiles/

# Create new profile
python integrated_preparedness_system.py --profile new_user
```

### Performance Issues
- **Clear Cache**: Use `--clear-cache` flag
- **Backup Cleanup**: Old backups auto-deleted
- **Database Optimization**: VACUUM periodically
- **Memory Usage**: Restart long-running processes

## 🛠️ Development

### Adding New Features
1. **Core Logic**: Add to `integrated_preparedness_system.py`
2. **CLI Support**: Update argument parser
3. **API Endpoint**: Add to `api_server.py` 
4. **GUI Interface**: Update `streamlit_gui.py`
5. **Profile Storage**: Modify `user_profile_manager.py`

### Testing
```bash
# Test CLI
python integrated_preparedness_system.py --status

# Test API
python api_server.py &
curl http://localhost:8000/health

# Test GUI  
streamlit run streamlit_gui.py
```

## 📋 Roadmap

### Phase 4: Advanced Features
- [ ] **Cloud Sync** - Multi-device synchronization
- [ ] **Mobile App** - React Native interface
- [ ] **Team Features** - Multi-user collaboration
- [ ] **Advanced Analytics** - ML-powered insights
- [ ] **IoT Integration** - Smart home sensors
- [ ] **Notification System** - SMS/Email alerts
- [ ] **Report Templates** - Custom report formats
- [ ] **API Rate Limiting** - Production security
- [ ] **Database Migration** - PostgreSQL support
- [ ] **Container Deployment** - Docker/Kubernetes

### Phase 5: Enterprise Features
- [ ] **SSO Integration** - LDAP/SAML support
- [ ] **Multi-tenant** - Organization management
- [ ] **Audit Logging** - Compliance features
- [ ] **Advanced Backup** - Cloud storage integration
- [ ] **Performance Monitoring** - Application metrics
- [ ] **Load Balancing** - High availability setup

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Implement** your changes
4. **Test** all interfaces (CLI, API, GUI)
5. **Submit** a pull request

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 📞 Support

For issues, questions, or feature requests:
- **GitHub Issues**: Create an issue
- **Documentation**: Check this README
- **API Docs**: Visit `/docs` when API server is running

---

**Emergency Preparedness System v3.0** - Complete disaster readiness platform with stateful operations, CLI interface, REST API, and web GUI. Be prepared for anything! 🚨