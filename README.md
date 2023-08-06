# NewsCrawlerAPI

NewsCrawlerAPI is a Flask-based API that allows crawling news articles using the newspaper3k library. It provides features such as pagination, ORM integration, authentication, and authorization.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication and Authorization](#authentication-and-authorization)
- [Contributing](#contributing)

## Features

- Crawling news articles from various sources using newspaper3k library.
- Pagination support for retrieving news articles in a paginated manner.
- ORM integration for storing and retrieving articles from a database.
- User authentication and authorization for secure access to API endpoints.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/NewsCrawlerAPI.git

2. Install the dependencies:
   ```
   pip install -r requirements.txt
 
3. Set up the database:
   ```
   flask db upgrade
## Usage

1. Access the API endpoints using the provided URL and port number (e.g., http://localhost:5000).

## API Endpoints

The following API endpoints are available:
- GET /articles: Retrieve a paginated list of articles.
- GET /articles/{id}: Retrieve details of a specific article.
- DELETE /articles/{id}: Delete an article from the database.
- POST /login: Authenticate and obtain an access token.
- POST /logout: Authenticate and obtain an access token.
- POST /create-user: for users to enter new news sources to crawl.
- POST /add-article: Crawler 100 articles according to 1 newspaper channel selected by the user.
- POST /crawl-article: Crawler 100 articles according to 1 newspaper channel selected by the user.

For detailed information on each endpoint and their request/response formats, refer to the API documentation.

## Authentication and Authorization

Authentication and authorization are implemented using JWT (JSON Web Tokens). To access protected API endpoints, include an Authorization header with the value Bearer <access_token>. The access token can be obtained by authenticating with valid credentials using the /login endpoint.

## Contributing

Contributions to NewsCrawlerAPI are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request. Make sure to follow the existing code style and conventions.

- Fork the repository.
- Create a new branch: git checkout -b my-feature.
- Make your changes and commit them: git commit -m 'Add new feature'.
- Push to the branch: git push origin my-feature.
- Submit a pull request.
