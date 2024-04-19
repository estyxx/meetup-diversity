# Meetup Diversity

This project is designed to analyze and visualize diversity data from the Django London Meetup group. It retrieves event details, extracts speaker names, and guesses the gender of speakers to provide insights into diversity trends within the community. Additionally, a Flask web server is utilized to handle OAuth redirections needed for Meetup API authentication.

## Inspiration

This project was inspired by the "Hidden Figures of Python" podcast series, which shines a light on lesser-known contributors in the Python community. Listening to these stories sparked curiosity about the diversity and representation within our community at the Django London Meetup. This project is a tribute to all the speakers who have shared their knowledge and expertise at our meetups.

[Listen to the Hidden Figures of Python](https://open.spotify.com/show/0paWD9BHs7QNNHsMFFUoIN)

## Features

- Fetch event data via the Meetup API using GraphQL.
- Extract speaker names from event descriptions.
- Predict speaker gender based on names.
- Save event data and analysis results in Excel and JSON formats.
- Flask web server to handle API redirects, with `ngrok` for local development.

## Installation

This project uses PDM (Python Development Master), a modern Python package manager with PEP 582 support, which means it doesn't require creating virtual environments in a traditional way.

### Prerequisites

- Python 3.12 or higher
- PDM for Python package management
- ngrok for secure tunneling to localhost

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/djangolondon-diversity.git
   cd djangolondon-diversity
   ```

2. **Install dependencies:**

   Using PDM, install the project dependencies by running:

   ```bash
   pdm install
   ```

3. **Set up ngrok:**

   - Sign up and download ngrok from [ngrok.com](https://ngrok.com).
   - Connect your account and start a tunnel to redirect to your local server:

     ```bash
     ngrok http http://127.0.0.1:5000
     ```

   - This will provide a URL that you will use as your `MEETUP_COM_REDIRECT_URI`. Every time you run the URL is slightly different, remember to update it in your Meetup API Settings.

## Usage

To run the project, you will need to start both the main script and the web server.

### Main Script

Execute the `main.py` script to start the data processing:

```bash
pdm run python main.py
```

### Web Server

Start the Flask web server to handle OAuth redirects:

```bash
pdm run python web_server.py
```

### Configuration

1. **Copy and Configure Environment Variables:**

   Copy the `.env.copy` file to `.env` and modify it to include your specific settings:

   ```plaintext
   MEETUP_COM_KEY=your_api_key_here
   MEETUP_COM_SECRET=your_secret_here
   MEETUP_COM_REDIRECT_URI="https://your-app.ngrok.io/redirect"
   OPENAI_API_KEY=your_open_ai_api_key_here
   ```

2. **Configure Meetup API Client:**

   - Visit the Meetup API settings page and set the redirect URI to the ngrok URL followed by `/redirect`.

### Output

The script will produce two types of files in the `outputs` directory:

- `events_data.xlsx`: An Excel file containing the events and speaker details including inferred genders.
- `events_data.json`: A JSON file with similar data, useful for web applications or further automated processing.

## Results and Observations

Upon running the script, you'll observe:

- The diversity of speakers based on gender over recent events.
- Patterns and trends that may assist in understanding diversity dynamics within the tech meetup community.

## Limitations

- **Accuracy of Gender Prediction**: The gender prediction is based solely on names using a heuristic approach and may not accurately reflect individuals' identities.
