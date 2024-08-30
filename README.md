# 💰 Smoobu Free Days Dealer: Maximize Your Occupancy with Smoobu API

Welcome to Smoobu Free Days Dealer, your intelligent assistant for identifying and filling gaps in your Smoobu apartment booking calendar!

## 📅 Project Overview

This Python-based system is a sophisticated, open-source toolkit designed to optimize your apartment bookings from the [Smoobu](https://www.smoobu.com/) platform. Its core feature is identifying free days between bookings and automatically sending targeted email campaigns to encourage guests to book those days, maximizing your occupancy and revenue.

This application brings together a task force of powerful components:

- **Smoobu Free Day Finder**: Intelligently identifies gaps between bookings using [Smoobu API](https://docs.smoobu.com/) 🔍
- **Automated Email Campaigns**: Sends personalized emails using [Jinja2](https://jinja.palletsprojects.com/) templates to entice guests to book free days 📧
- **Comprehensive Reporting**: Generates reports on occupancy rates and revenue 📈

This system is powered by:

- **SmoobuAPIClient**: Communicates with the Smoobu API using the [requests](https://docs.python-requests.org/) library
- **SmoobuService**: Orchestrates data retrieval, processing, and updating
- **Formatters**: Transforms raw booking data into actionable insights
- **DTOs**: Ensures data consistency and type safety

Additional tools in our booking optimization toolkit:

- **logging**: Maintains detailed system logs
- **caching**: Optimizes API usage with [cachetools](https://pypi.org/project/cachetools/)
- **rate limiting**: Ensures compliance with API constraints using [ratelimit](https://pypi.org/project/ratelimit/)

## 🛠️ Installation

To set up your own Smoobu Free Days Dealer:

1. Clone this revenue-boosting repository:
   ```
   git clone https://github.com/otenmoten/bot-smoobu-free-days-dealer.git
   ```
2. Enter the project directory:
   ```
   cd bot-smoobu-free-days-dealer
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. Configure your Smoobu connection and email settings:
   ```
   config.py
   ```

2. Start boosting your bookings:
   ```
   python main.py
   ```

## 📜 License

This project is licensed under the GPL3.0 License - see the [LICENSE](LICENSE) file for details.

## 👨‍💼 Authors

- Kevin Ossenbrück - Lead Developer at Team Bitfuture - [ossenbrück.de](https://ossenbrück.de)

## 🤝 Connect with Team BitFuture

- Website: [team-bitfuture.de](https://team-bitfuture.de)
- E-mail: [info@team-bitfuture.de](mailto:info@team-bitfuture.de)

Start maximizing your occupancy and revenue today with Smoobu Free Days Dealer! 💼🏠