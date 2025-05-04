import logging
from playwright.sync_api import expect
import utils.custom_logger as cl
import time
import os

class PlaywrightDriver:

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, page):
        self.page = page

    def screenShot(self, resultMessage):
        """
        Takes screenshot of the current open web page
        """
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = "../screenshots/"
        relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.page.screenshot(path=destinationFile)
            self.log.info("Screenshot save to directory: " + destinationFile)
        except:
            self.log.error("### Exception Occurred when taking screenshot")

    def getByLocatorType(self, locatorType, locator):
        try:
            locator_type = locatorType.lower()
            if locator_type == "role":
                return self.page.get_by_role(locator)
            elif locator_type == "text":
                return self.page.get_by_text(locator)
            elif locator_type == "label":
                return self.page.get_by_label(locator)
            elif locator_type == "placeholder":
                return self.page.get_by_placeholder(locator)
            elif locator_type == "alt_text":
                return self.page.get_by_alt_text(locator)
            elif locator_type == "title":
                return self.page.get_by_title(locator)
            elif locator_type == "test_id":
                return self.page.get_by_test_id(locator)
            elif locator_type == "id":
                return self.page.locator(locator)
            elif locator_type == "xpath":
                return self.page.locator(locator)
            elif locator_type == "css":
                return self.page.locator(locator)
            else:
                self.log.info("Locator type " + locatorType +
                              " not correct/supported")
                raise ValueError(f"Unsupported locator type: {locator_type}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while locating the element: {e}")

    def getTitle(self):
        try:
            title = self.page.title()
            if title is not None:
                self.log.info("Page title is: " + title)
            else:
                self.log.info("Page title not found")
        except Exception as e:
            raise RuntimeError(f"An error occurred while getting the page title: {e}")
        return title

    def getElement(self, locatorType, locator):
        try:
            locatorType = locatorType.lower()
            element =  self.getByLocatorType(locatorType, locator)
            if element is not None:
                self.log.info("Element found with locator: " + locator +
                              " and  locatorType: " + locatorType)
            else:
                self.log.info("Element not found with locator: " + locator +
                              " and  locatorType: " + locatorType)
        except Exception as e:
            raise RuntimeError(f"An error occurred while getting the element: {e}")
        return element

    def elementClick(self, locatorType, locator):
        try:
            element = self.getElement(locatorType, locator)
            if element is not None:
                element.click()
                self.log.info("Clicked on element with locator: " + locator +
                            " locatorType: " + locatorType)
            else:
                self.log.info("Element not found to click: " + locator +
                              " locatorType: " + locatorType)
        except Exception as e:
            raise RuntimeError(f"An error occurred while clicking the element: {e}")

    def isElementPresent(self, locatorType, locator):
        try:
            element = self.getElement(locatorType, locator)
            if element is not None:
                self.log.info("Element Found: " + locator +
                              " locatorType: " + locatorType)
                return True
            else:
                self.log.info("Element not found: " + locator +
                              " locatorType: " + locatorType)
                return False
        except Exception as e:
            raise RuntimeError(f"An error occurred while checking if the element is present: {e}")

    def waitForElement(self, locatorType, locator, timeout=10):
        try:
            element = self.getElement(locatorType, locator)
            element.wait_for(timeout=timeout * 1000)
            if element is not None:
                self.log.info("Element appeared on the web page: " + locator +
                              " locatorType: " + locatorType)
            else:
                self.log.info("Element not appeared on the web page: " + locator +
                              " locatorType: " + locatorType)
        except Exception as e:
            raise RuntimeError(f"An error occurred while waiting for the element: {e}")
        return element

    def sendKeys(self, locatorType, locator, text):
        try:
            element = self.getElement(locatorType, locator)
            if element is not None:
                element.fill(text)
                self.log.info("Sent text to the element with locator: " + locator +
                              " locatorType: " + locatorType)
            else:
                self.log.info("Element not found to send text: " + locator +
                              " locatorType: " + locatorType)
        except Exception as e:
            raise RuntimeError(f"An error occurred while sending keys to the element: {e}")

    def clearField(self, locatorType, locator):
        try:
            element = self.getElement(locatorType, locator)
            if element is not None:
                element.fill("")
                self.log.info("Cleared the field with locator: " + locator +
                              " locatorType: " + locatorType)
            else:
                self.log.info("Element not found to clear field: " + locator +
                              " locatorType: " + locatorType)
        except Exception as e:
            raise RuntimeError(f"An error occurred while clearing the field: {e}")

    def expect_title(self, title, timeout=10, retries=3):
        for attempt in range(retries):
            try:
                for _ in range(timeout):
                    try:
                        if title in self.getTitle():
                            self.log.info(f"Page title matched: {title}")
                            return True
                    except Exception as e:
                        self.log.warning(f"Retrying due to error: {e}")
                    self.page.wait_for_timeout(1000)  # Wait for 1 second
            except Exception as e:
                self.log.error(f"Attempt {attempt + 1} failed: {e}")
            self.log.info(f"Retrying... ({attempt + 1}/{retries})")
        return False

    def expect_element_visible(self, locatorType, locator):
        try:
            element = self.getElement(locatorType, locator)
            if element is not None:
                expect(element).to_be_visible()
                self.log.info("Element is visible: " + locator +
                              " locatorType: " + locatorType)
                return True
            else:
                self.log.info("Element not found to check visibility: " + locator +
                              " locatorType: " + locatorType)
                return False

        except Exception as e:
            raise RuntimeError(f"An error occurred while checking if the element is visible: {e}")

    def expect_element_not_visible(self, locatorType, locator):
        try:
            element = self.getElement(locatorType, locator)
            if element is not None:
                expect(element).not_to_be_visible()
                self.log.info("Element is not visible: " + locator +
                              " locatorType: " + locatorType)
            else:
                self.log.info("Element not found to check visibility: " + locator +
                              " locatorType: " + locatorType)
        except Exception as e:
            raise RuntimeError(f"An error occurred while checking if the element is not visible: {e}")

    def expect_element_enabled(self, locatorType, locator):
        try:
            element = self.getElement(locatorType, locator)
            if element is not None:
                expect(element).to_be_enabled()
                self.log.info("Element is enabled: " + locator +
                              " locatorType: " + locatorType)
            else:
                self.log.info("Element not found to check enabled state: " + locator +
                              " locatorType: " + locatorType)
        except Exception as e:
            raise RuntimeError(f"An error occurred while checking if the element is enabled: {e}")

    def expect_element_disabled(self, locatorType, locator):
        try:
            element = self.getElement(locatorType, locator)
            if element is not None:
                expect(element).not_to_be_enabled()
                self.log.info("Element is disabled: " + locator +
                              " locatorType: " + locatorType)
            else:
                self.log.info("Element not found to check disabled state: " + locator +
                              " locatorType: " + locatorType)
        except Exception as e:
            raise RuntimeError(f"An error occurred while checking if the element is disabled: {e}")

    def expect_to_have_text(self, locatorType, locator, text):
        try:
            element = self.getElement(locatorType, locator)
            if element is not None:
                expect(element).to_have_text(text)
                self.log.info("Element has text: " + text +
                              " locatorType: " + locatorType)
            else:
                self.log.info("Element not found to check text: " + locator +
                              " locatorType: " + locatorType)
        except Exception as e:
            raise RuntimeError(f"An error occurred while checking the text of the element: {e}")

    def scroll_element_into_view(self, locatorType, locator):
        try:
            element = self.getElement(locatorType, locator)
            if element is not None:
                element.page.scroll_into_view_if_needed()
                self.log.info("Scrolled to the element: " + locator +
                              " locatorType: " + locatorType)
            else:
                self.log.info("Element not found to scroll: " + locator +
                              " locatorType: " + locatorType)
        except Exception as e:
            raise RuntimeError(f"An error occurred while scrolling to the element: {e}")

    def getElementList(self, locatorType, locator):
        """
        Get list of elements using locator

        Parameters:
            1. Required:
                locator   - Locator of the element
            2. Optional:
                locatorType - Locator Type to find the element
        Returns:
            List of elements
        Exception:
            None
        """
        try:
            elements = self.getByLocatorType(locatorType, locator).all()
            if len(elements) > 0:
                self.log.info("Element list FOUND with locator: " + locator +
                              " and locatorType: " + locatorType)
            else:
                self.log.info("Element list NOT FOUND with locator: " + locator +
                              " and locatorType: " + locatorType)
            return elements
        except Exception as e:
            raise RuntimeError(f"An error occurred while getting the element list: {e}")

    def switchToFrame(self, framelocator):
        try:
            frame = self.page.frame_locator(framelocator)
            if frame is not None:
                self.page.frame_locator(framelocator)
                self.log.info("Switched to frame: " + framelocator)
            else:
                self.log.info("Frame not found: " + framelocator)
        except Exception as e:
            raise RuntimeError(f"An error occurred while switching to the frame: {e}")
        return frame

    def getElementAttributeValue(self, locatorType, locator, attribute):
        try:
            element = self.getElement(locatorType, locator)
            value = element.get_attribute(attribute)
            self.log.info(f"Element attribute value: {value}")
            return value
        except Exception as e:
            raise RuntimeError(f"An error occurred while getting the element attribute value: {e}")

    def selectElementFromDropDown(self, locatorType, locator, value):
        try:
            element = self.getElement(locatorType, locator)
            if element is not None:
                element.select_option(value)
                self.log.info("Selected value from dropdown: " + value +
                              " locatorType: " + locatorType)
            else:
                self.log.info("Element not found to select from dropdown: " + locator +
                              " locatorType: " + locatorType)
        except Exception as e:
            raise RuntimeError(f"An error occurred while selecting from the dropdown: {e}")





