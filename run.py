from src import data_grabber, data_cleaner, db_accessor, log_configs
import logging
import json


# app = create_app()
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port="5000")


def main():
    log_configs.setup_logging()
    logger = logging.getLogger(__name__)
    # data_grabber.get_data()
    raw_data = data_grabber.html_scrubber()
    # with open("tests/mock_data.json") as f:
    #     raw_data = json.load(f)
    aide_data, shift_data = data_cleaner.clean(raw_data)
    db_accessor.add_aides_to_db(aide_data)
    db_accessor.add_shifts_to_db(shift_data)

    # with open("tests/updated_data.json") as f:
    #     raw_data = json.load(f)
    # aide_data, shift_data = data_cleaner.clean(raw_data)
    # db_accessor.add_aides_to_db(aide_data)
    # db_accessor.add_shifts_to_db(shift_data)
    # web_hosting.run()


if __name__ == "__main__":
    main()
