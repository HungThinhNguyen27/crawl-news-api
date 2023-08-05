from flask import jsonify


class employer:

    @staticmethod
    def token_revoked():
        return jsonify({"message": "Token revoked"}), 401

    @staticmethod
    def token_expired():
        return jsonify({"message": "Token expired"}), 401

    @staticmethod
    def invalid_token():
        return jsonify({"message": "Token invalid"}), 401

    @staticmethod
    def valid_token():
        return jsonify({"message": "valid token"}), 401

    @staticmethod
    def log_out_success():
        return jsonify({"message": "Log out success"}), 200

    @staticmethod
    def invalid_username_or_password():
        return jsonify({"error": "Invalid username or password"}), 401

    @staticmethod
    def username_already_exists():
        return jsonify({"error": "Username already exists"}), 400

    @staticmethod
    def invalid_role(role):
        return jsonify({"error": "Invalid {} role ".format(role)}), 400

    @staticmethod
    def create_account_success(username):
        return (
            jsonify({"message": "Account {} created successfully".format(username)}),
            201,
        )

    @staticmethod
    def username_already_exists(username):
        return jsonify({"message": "Username {} already exists".format(username)}), 201

    @staticmethod
    def no_token_provided():
        return jsonify({"error": "No token provided"}), 400

    @staticmethod
    def unauthorized():
        return jsonify({"Message": "you do not have access to this resource."}), 401

    @staticmethod
    def employer_deleted(id):
        return jsonify({"message": "Employer with id {} has been deleted".format(id)})

    @staticmethod
    def employer_not_found(id):
        return jsonify({"message": "Employer with {} not found".format(id)}), 404

    @staticmethod
    def update_success(employer_edit):
        return jsonify({"message": "User information updated successfully {}".format(employer_edit)}), 404

    @staticmethod
    def update_failed(employer_edit):
        return jsonify({"message": "Failed to update user information. {}".format(employer_edit)}), 404


class articles:

    @staticmethod
    def invalid_page_number():
        return jsonify({"message": "Invalid page number"}), 400

    @staticmethod
    def page_doesnt_exist():
        return jsonify({"message": "This page does not exist"}), 400

    @staticmethod
    def invalid_limit_number():
        return jsonify({"message": "Invalid limit number"}), 400

    @staticmethod
    def Invalid_URL_format():
        return jsonify({"error": "Invalid URL format"}), 400

    @staticmethod
    def article_deleted(id):
        return jsonify({"message": "Article with id {} has been deleted".format(id)})

    @staticmethod
    def article_not_found(id):
        return jsonify({"message": "Article with {} not found".format(id)}), 404

    @staticmethod
    def created_successfully(name_article, url):
        return (
            jsonify(
                {
                    "message": " a newspaper page has been added successfully",
                    "newspaper page": {"name": name_article, "url": url},
                }
            ),
            201,
        )

    @staticmethod
    def articles_name_exists(name_article, url):
        return (
            jsonify(
                {
                    "message": "  a newspaper page already axists",
                    "newspaper page": {"name": name_article, "url": url},
                }
            ),
            201,
        )

    @staticmethod
    def article_format(article_dict):
        return jsonify({"article": article_dict}), 200

    @staticmethod
    def article_crawling():
        return jsonify({"message": "Article crawling......"}), 200

    @staticmethod
    def url_not_provided(id):
        return jsonify({"error": "URL not provided"}), 400

    @staticmethod
    def add_success():
        return jsonify({"message": "Du lieu da duoc them vao index "}), 200
