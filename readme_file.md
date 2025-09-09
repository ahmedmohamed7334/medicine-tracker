# 💊 Medicine Tracker

A user-friendly medication tracking web application built with Streamlit, designed to help elderly patients keep track of their daily medications with simple click-to-confirm functionality.

## 🌟 Features

- **Simple Interface**: Large buttons and clear status indicators for easy use
- **Daily Tracking**: Track morning, afternoon, and evening medications
- **Status Management**: Mark medications as taken, pending, missed, or skipped
- **History Viewing**: View medication history and compliance rates
- **Automatic Status Updates**: Medications automatically marked as "missed" after 2-hour grace period
- **Progress Tracking**: Daily progress bars and summary statistics
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 📋 Medication Schedule

The application tracks the following medications:

### Morning Medications (6 AM - 3 PM)
- Controloc (8:00 AM) - Before breakfast
- Sandocal Vitamin D (8:30 AM) - With breakfast
- Symbicort Inhaler (8:00 AM)
- Cervitam (9:00 AM)
- Milga Advance (9:00 AM) - Diabetes support
- Magnesium (9:30 AM)
- Potassium Drink (10:00 AM)
- Dermovate Cream (11:00 AM)
- Fast Freeze Gel (12:00 PM)
- Movxir (1:00 PM)
- Januvia (2:00 PM) - After lunch

### Evening Medications (3 PM - 11:59 PM)
- Symbicort Inhaler (8:00 PM)
- Cervitam (9:00 PM)
- Tebonina Forte (9:00 PM)
- Lipostat (10:00 PM) - Before bed
- Dermovate Cream (11:00 PM)

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/medicine-tracker.git
   cd medicine-tracker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run main.py
   ```

4. **Open your browser** to `http://localhost:8501`

### Deploy to Streamlit Cloud

1. **Fork this repository** to your GitHub account
2. **Go to** [share.streamlit.io](https://share.streamlit.io)
3. **Connect your GitHub account** and select this repository
4. **Set the main file path** to `main.py`
5. **Deploy** - Your app will be live in minutes!

## 📁 Project Structure

```
medicine-tracker/
├── main.py                 # Main Streamlit application
├── database.py            # Database management and operations
├── medication_config.py   # Medication schedules and configuration
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── medication_tracker.db # SQLite database (created automatically)
```

## 🔧 Configuration

### Adding New Medications

To add new medications, edit the `medication_config.py` file:

```python
MEDICATIONS = {
    'new_medicine': {
        'name': 'New Medicine Name',
        'times': [time(9, 0), time(21, 0)],  # 9 AM and 9 PM
        'instructions': 'Take twice daily with food'
    }
}
```

### Modifying Schedules

You can easily modify medication times by updating the `times` array in the configuration:

```python
'times': [time(8, 0), time(20, 0)]  # 8 AM and 8 PM
```

## 💾 Database

The application uses SQLite for local data storage. The database automatically:

- **Creates tables** on first run
- **Stores medication records** with timestamps
- **Tracks compliance** over time
- **Maintains history** for reporting

### Database Schema

```sql
medication_records (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    medication_key TEXT NOT NULL,
    status TEXT CHECK (status IN ('taken', 'missed', 'pending', 'skipped')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, medication_key)
)
```

## 🎨 User Interface

### Status Indicators
- 🟢 **Taken** - Medication has been taken
- 🟡 **Pending** - Waiting to be taken
- 🔴 **Missed** - Past due (2+ hours after scheduled time)
- ⚪ **Skipped** - Intentionally skipped

### Navigation
- **Today's Medicines** - Current day medication tracking
- **History** - View past medication records and compliance
- **Add Medicine** - Configuration overview (future feature)

## 🔒 Privacy & Security

- **Local Storage**: All data stored locally in SQLite database
- **No External APIs**: No medication data sent to external services
- **Self-Hosted**: Run on your own infrastructure
- **No User Authentication**: Designed for single-user household use

## 📱 Mobile Friendly

The application is fully responsive and works well on:
- ✅ Desktop computers
- ✅ Tablets
- ✅ Smartphones
- ✅ Large button design for elderly users

## 🆘 Support

### Common Issues

**Database not creating**: Make sure the application has write permissions in the directory.

**Times not displaying correctly**: Check timezone settings on your system.

**Medications not showing**: Verify the `medication_config.py` file syntax.

### Getting Help

1. Check the [Issues](https://github.com/your-username/medicine-tracker/issues) page
2. Create a new issue with detailed description
3. Include error messages and screenshots if applicable

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin new-feature`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for rapid web app development
- Uses SQLite for reliable local data storage
- Designed with elderly users in mind for accessibility

## 📞 Contact

For questions or support, please open an issue on GitHub or contact the development team.

---

**Made with ❤️ for better health management**