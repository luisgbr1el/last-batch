# Last.Batch

Desktop application for batch scrobbling to Last.fm. Process CSV files with playback history and send them to your Last.fm account.

## Features

- Last.fm authentication
- Batch processing (CSV, TXT, JSON)
- Preview and edit scrobbles before sending
- Real-time progress tracking
- Multi-language support (English, Português)

## Setup

1. Get Last.fm API credentials at [https://www.last.fm/api/account/create](https://www.last.fm/api/account/create)

2. Create a `.env` file:
```env
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run:
```bash
python src/main.py
```

## File formats

- **.csv** with 3 columns: Artist, Track, Timestamp

    ```csv
    The Beatles,Yesterday,2024-01-01 12:00:00
    Pink Floyd,Wish You Were Here,2024-01-01 13:30:00
    ```

## Usage

1. Authenticate with Last.fm
2. Upload your file
3. Review scrobbles (press Delete to remove items)
4. Click Scrobble

## Build executable

```bash
pyinstaller Last.Batch.spec
```

## Author

Developed by [luisgbr1el](https://github.com/luisgbr1el)