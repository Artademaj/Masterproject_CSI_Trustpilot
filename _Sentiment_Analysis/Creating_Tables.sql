--SQL Commands Trustpilot project

-- NOTE: the path behind every \copy command needs to be adjusted to the one that applies to your computer!

--Table sustainability words 
CREATE TABLE IF NOT EXISTS sustainability_words(
social_sustainability text,
environmental_sustainability text,
economic_sustainability text
);

\copy sustainability_words FROM '/Users/Arta/_Sentiment_Analysis/sustainanbility_words.csv' delimiter ',' csv header;


--Table S&P500 companies dataset
CREATE TABLE IF NOT EXISTS list_companies(
Symbol text,
Company text,
Subsidiaries text,
Sector text,
Price text,
Price_Earnings text,
Dividend_Yield text,
Earnings_Share text,
Market_Cap text,
EBITDA text,
Price_Sales text,
Price_Book text,
SEC_Filings text
);

\copy list_companies FROM '/Users/Arta/_Sentiment_Analysis/S&P_companies.csv' delimiter ',' csv header;


--Tables review datasets

CREATE TABLE IF NOT EXISTS reviews_food_beverages_tobacco(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_food_beverages_tobacco FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_food_beverages_tobacco.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_business_services(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_business_services FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_business_services.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_animals_pets(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_animals_pets FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_animals_pets.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_beauty_wellbeing(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_beauty_wellbeing FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_beauty_wellbeing.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_construction_manufactoring(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_construction_manufactoring FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_construction_manufactoring.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_education_training(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_education_training FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_education_training.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_events_entertainment(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_events_entertainment FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_events_entertainment.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_health_medical(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_health_medical FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_health_medical.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_hobbies_crafts(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_hobbies_crafts FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_hobbies_crafts.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_home_garden(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_home_garden FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_home_garden.csv' delimiter ',' csv header;


CREATE TABLE IF NOT EXISTS reviews_electronics_technology(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_electronics_technology FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_electronics_technology.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_home_services(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_home_services FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_home_services.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_legal_services_government(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_legal_services_government FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_legal_services_government.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_media_publishing(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_media_publishing FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_media_publishing.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_money_insurance(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_money_insurance FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_money_insurance.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_public_local_services(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_public_local_services FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_public_local_services.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_restaurants_bars(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_restaurants_bars FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_restaurants_bars.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_shopping_fashion(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_shopping_fashion FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_shopping_fashion.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_sports(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_sports FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_sports.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_travel_vacation(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_travel_vacation FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_travel_vacation.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_utilities(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_utilities FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_utilities.csv' delimiter ',' csv header;

CREATE TABLE IF NOT EXISTS reviews_vehicles_transportation(
Company text,
Category text,
total_reviews text,
general_rating text,
review_rating text,
review_text text
);

\copy reviews_vehicles_transportation FROM '/Users/Arta/_trustpilot/trustpilot/spiders/reviews_vehicles_transportation.csv' delimiter ',' csv header;