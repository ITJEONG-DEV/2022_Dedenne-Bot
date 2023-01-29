import datetime
from PIL import Image, ImageDraw, ImageFont


# island = [ "하모니 섬", "죽음의 협곡", "고요한 안식의 섬" ]
# reward = [ "카드", "실링", "골드" ]
def get_adventure_island(island, reward, double=False):
    title_size = (460 * 3, 120)
    island_size = (460, 290)
    reward_size = (460, 260)
    content_size = (460, 290 + 260)

    now = datetime.datetime.now()
    font = ImageFont.truetype("C:/USERS/DEV2/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/NANUMBARUNGOTHICBOLD.TTF", size=30)
    background_color = (0, 0, 0)
    font_color = (255, 255, 255)

    if double:
        width = title_size[0]
        height = (title_size[1] + island_size[1] + reward_size[1]) * 2

        image = Image.new('RGB', (width, height), background_color)

        for j in range(2):
            # paste content
            for i in range(3):
                island_image = Image.open(f'lostark/adventure_island/data/island/{island[i+j*3]}.jpg')
                island_image = island_image.resize(island_size)

                reward_image = Image.open(f'lostark/adventure_island/data/reward/{reward[i+j*3]}.jpg')
                reward_image = reward_image.resize(reward_size)

                new_image = Image.new('RGB', content_size)
                new_image.paste(island_image, (0, 0))
                new_image.paste(reward_image, (0, 290))

                image.paste(new_image, (460 * i, title_size[1] + int(height/2 * j)))

            # add title
            drawable_image = ImageDraw.Draw(image)
            title = now.strftime("%Y-%m-%d") + " 모험섬"
            if j == 0:
                title += " 오전 타임 (09:00/11:00/13:00)"
            elif j == 1:
                title += " 오후 타임 (19:00/21:00/23:00)"

            w, h = drawable_image.textsize(title, font=font)
            x, y = (title_size[0] - w) / 2, (title_size[1] + height * j - h) / 2
            drawable_image.text((x, y), title, fill=font_color, font=font)

    else:
        width = title_size[0]
        height = (title_size[1] + island_size[1] + reward_size[1])

        image = Image.new('RGB', (width, height), background_color)

        # paste content
        for i in range(3):
            island_image = Image.open(f'lostark/adventure_island/data/island/{island[i]}.jpg')
            island_image = island_image.resize(island_size)

            reward_image = Image.open(f'lostark/adventure_island/data/reward/{reward[i]}.jpg')
            reward_image = reward_image.resize(reward_size)

            new_image = Image.new('RGB', content_size)
            new_image.paste(island_image, (0, 0))
            new_image.paste(reward_image, (0, 290))

            image.paste(new_image, (460 * i, title_size[1]))

        # add title
        drawable_image = ImageDraw.Draw(image)
        title = now.strftime("%Y-%m-%d") + " 모험섬 (11:00/13:00/19:00/21:00/23:00)"
        w, h = drawable_image.textsize(title, font=font)
        x, y = (title_size[0] - w) / 2, (title_size[1] - h) / 2
        drawable_image.text((x, y), title, fill=font_color, font=font)

    link = f'lostark/adventure_island/data/today/{now.strftime("%Y%m%d")}.jpg'
    image.save(link)

    # return image
    return link


if __name__ == "__main__":
    image = get_adventure_island(
        island=["하모니 섬", "죽음의 협곡", "고요한 안식의 섬", "하모니 섬", "죽음의 협곡", "고요한 안식의 섬"],
        reward=["카드", "실링", "골드", "카드", "실링", "골드"],
        double=False
    )

    # image.show()
