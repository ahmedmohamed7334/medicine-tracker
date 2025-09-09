# 💊 Medication Tracker

A user-friendly web application built with Streamlit to help track daily medication intake. Perfect for elderly users or anyone who needs to maintain a medication schedule.

## Features

- **Simple Interface**: Large buttons and clear visual indicators
- **Mobile Friendly**: Responsive design that works well on phones and tablets
- **Daily Tracking**: Track morning and evening medications
- **Status Indicators**: Clear visual feedback (Taken ✓, Missed ✗, Pending ⏳)
- **History View**: Review past medication records
- **Automatic Database**: SQLite database automatically manages all data
- **Pre-configured Medications**: Comes with your mother's medication list pre-loaded

## Medications Included

The app comes pre-configured with these medications:
- Cervitam (twice daily)
- Tebonina Forte (twice daily)
- Symbicort Inhaler (twice daily)
- Fast Freeze Gel (twice daily)
- Movxir (twice daily)
- Potassium Drink (once daily)
- Milga Advance (once daily)
- Januvia (once daily, after lunch)
- Lipostat (once nightly)
- Controloc (once morning)
- Dermovate Cream (twice daily, 10-day course)
- Sandocal Vitamin D (once morning)
- Magnesium (once morning)

## Quick Start

### Local Development

1. Clone this repository:
```bash
git clone <your-repo-url>
cd medication-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push this code to your GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository and `app.py` as the main file
5. Deploy!

## How to Use

### Daily Medication Tracking

1. Open the app - you'll see today's medications
2. Each medication shows its schedule and current status
3. Click "✓ Taken" when medication is consumed
4. Click "✗ Missed" if medication was skipped
5. Status updates immediately with color-coded indicators

### Viewing History

1. Use the sidebar to select any date
2. Click "View History" to see past records
3. Click "Today's Overview" to return to daily tracking

### Mobile Usage

- The app is optimized for mobile devices
- Large touch-friendly buttons
- Responsive design that adapts to screen size
- Easy navigation with simple gestures

## File Structure

```
medication-tracker/
│
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── medication_tracker.db  # SQLite database (auto-created)
```

## Database Schema

The app uses SQLite with two main tables:

- **medications**: Stores medication information
- **medication_logs**: Tracks when medications are taken/missed

## Customization

To modify medications, edit the `init_default_medications()` function in `app.py`. The format is:
```python
("Medication Name", "Schedule Description", times_per_day, "Special Instructions")
```

## Technical Details

- **Framework**: Streamlit
- **Database**: SQLite (no external database required)
- **Styling**: Custom CSS for mobile-friendly design
- **State Management**: Streamlit session state
- **Data Storage**: Local SQLite file (persistent across sessions)

## Troubleshooting

### Common Issues

1. **App won't start**: Ensure all dependencies are installed
2. **Database errors**: Delete `medication_tracker.db` to reset
3. **Mobile display issues**: Clear browser cache

### Support

For technical issues or feature requests, please create an issue in the GitHub repository.

## License

This project is open source and available under the MIT License.

---

**Built with ❤️ for better medication management**