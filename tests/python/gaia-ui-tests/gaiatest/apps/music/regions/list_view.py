# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import expected, By, Wait

from gaiatest.apps.base import Base, PageRegion
from gaiatest.apps.music.regions.sublist_view import AlbumSublistView, ArtistSublistView
from gaiatest.apps.music.regions.player_view import PlayerView


class ListView(Base):

    _list_item_locator = (By.CLASS_NAME, 'gfl-item')

    def _set_active_view(self, type):
        self._active_view_locator = (By.CSS_SELECTOR, 'iframe.active[src*="/views/{}/index.html"]'.format(type))

    @property
    def media(self):
        self.marionette.switch_to_frame(self.marionette.find_element(*self._active_view_locator))
        elements = Wait(self.marionette).until(
            expected.elements_present(*self._list_item_locator))
        Wait(self.marionette).until(expected.element_displayed(elements[0]))
        return [Media(self.marionette, element) for element in elements]


class AlbumsView(ListView):
    def __init__(self, marionette):
        ListView.__init__(self, marionette)
        self._set_active_view('albums')


class ArtistsView(ListView):
    def __init__(self, marionette):
        ListView.__init__(self, marionette)
        self._set_active_view('artists')


class SongsView(ListView):
    def __init__(self, marionette):
        ListView.__init__(self, marionette)
        self._set_active_view('songs')


class Media(PageRegion):
    _first_media_link_locator = (By.CLASS_NAME, 'gfl-item first')

    def tap_first_album(self):
        self.marionette.find_element(*self._first_media_link_locator).tap()
        self.apps.switch_to_displayed_app()
        return AlbumSublistView(self.marionette)

    def tap_first_song(self):
        self.marionette.find_element(*self._first_media_link_locator).tap()
        self.apps.switch_to_displayed_app()
        return PlayerView(self.marionette)

    def tap_first_artist(self):
        self.marionette.find_element(*self._first_media_link_locator).tap()
        self.apps.switch_to_displayed_app()
        return ArtistSublistView(self.marionette)

    def a11y_click_first_album(self):
        self.accessibility.click(
            self.marionette.find_element(*self._first_media_link_locator))
        self.apps.switch_to_displayed_app()
        return AlbumSublistView(self.marionette)