import pytest
from selenium.webdriver.common.by import By
from tests.conftest import request_dataset
import time
import server


@pytest.mark.usefixtures("setup")
class TestServer:
    def test_login_and_logout(self):
        index_url = self.driver.current_url
        title_page = self.driver.title
        club, competition = request_dataset(0, 0)
        login_text_box = self.driver.find_element(By.XPATH, "/html/body/form/input")
        login_text_box.click()
        login_text_box.send_keys(club['email'])
        btn = self.driver.find_element(By.XPATH, "/html/body/form/button")
        btn.click()

        welcome_url = self.driver.current_url
        welcome_title_page = self.driver.title
        welcome_text_h2 = self.driver.find_element(By.XPATH, "/html/body/h2").text
        time.sleep(5)

        logout_link = self.driver.find_element(By.XPATH, "/html/body/a")
        logout_link.click()
        logout_url = self.driver.current_url

        assert title_page == "GUDLFT Registration"
        assert "showSummary" in welcome_url
        assert welcome_title_page == "Summary | GUDLFT Registration"
        assert club['email'] in welcome_text_h2
        assert logout_url == index_url

    def test_login_and_books_places(self):
        club, competition = request_dataset(0, 0)
        login_text_box = self.driver.find_element(By.XPATH, "/html/body/form/input")
        login_text_box.click()
        login_text_box.send_keys(club['email'])
        btn = self.driver.find_element(By.XPATH, "/html/body/form/button")
        btn.click()

        link_booking = self.driver.find_element(By.XPATH, "/html/body/ul/li[1]/a")
        link_booking.click()
        booking_url = self.driver.current_url
        booking_competition_h2 = self.driver.find_element(By.XPATH, "/html/body/h2").text
        input_number_places = self.driver.find_element(By.XPATH, "/html/body/form/input[3]")
        input_number_places.click()
        input_number_places.send_keys("1")
        btn_booking = self.driver.find_element(By.XPATH, "/html/body/form/button")
        btn_booking. click()

        link_purchasePlace = self.driver.current_url
        purchase_welcome_h2 = self.driver.find_element(By.XPATH, "/html/body/h2").text
        purchase_valid_message = self.driver.find_element(By.XPATH, "/html/body/ul[1]/li").text
        club_points_remaining = self.driver.find_element(By.XPATH, "/html/body").text
        remaining_points = int(club['points']) - server.COST_PLACE
        remaining_points_msg = f"Points available: {remaining_points}"
        competition_places_remaining = self.driver.find_element(By.XPATH, "/html/body/ul[2]/li[1]").text
        remaining_places = int(competition["numberOfPlaces"])-1
        remaining_places_msg = f"Number of Places: {remaining_places}"

        assert competition['name'].replace(" ", "%20") in booking_url
        assert club['name'].replace(" ", "%20") in booking_url
        assert "/book/" in booking_url
        assert competition['name'] in booking_competition_h2
        assert "purchasePlaces" in link_purchasePlace
        assert club['email'] in purchase_welcome_h2
        assert "Great-booking complete" in purchase_valid_message
        assert remaining_points_msg in club_points_remaining
        assert remaining_places_msg in competition_places_remaining
