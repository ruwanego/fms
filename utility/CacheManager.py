""" Cache Manager

This module covers initializing system, install update fonts, database
manipulation like operations.

Created by Lahiru Pathirage @ Mooniak<lpsandaruwan@gmail.com> on 2/12/2016
"""

import requests

from consumer import GitHubConsumer
from service import ChannelService, FontIndexService, FontService, \
    GithubFontService


class CacheManager:

    def __init__(self):
        self.__channel_service = ChannelService()
        self.__font_index_service = FontIndexService()
        self.__font_service = FontService()
        self.__github_font_service = GithubFontService()

    def update_github_font_cache(self):
        channels = self.__channel_service.find_by_channel_type("github")

        for channel in channels:
            # get fonts list from channel
            fonts_list = requests.get(channel.base_url).json()

            # update fonts information
            for font in fonts_list:
                # get font data using github API
                latest_release = GitHubConsumer(
                    font["branch"], font["repository"], font["user"]
                ).get_latest_release_info()

                # add a record in fonts directory
                self.__font_service.add_new(
                    font["id"],
                    channel.channel_id,
                    font["name"],
                    latest_release["zipball_url"],
                    latest_release["tag_name"]
                )

                # add a detailed infromation record in github fonts table
                self.__github_font_service.add_new(
                    font["id"],
                    font["branch"],
                    font["path"],
                    font["repository"],
                    font["user"]
                )

                # add a record in font index
                self.__font_index_service.add_new(
                    font["id"], False, False
                )
