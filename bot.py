import discord
import time
import os
import datetime
from cv2 import cv2


TOKEN = "YOUR_BOT_TOKEN"

client = discord.Client()


async def grayscale_pic(file_path):
    im = cv2.imread(file_path, 0)
    cv2.imwrite("ass_" + file_path, im)
    os.remove(file_path)
    return "ass_" + file_path


async def grayscale_video(file_path):
    start = time.time()
    print("video read")
    video = cv2.VideoCapture(file_path)

    if video.isOpened() == False:
        print("Error reading video file")

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    size = (frame_width, frame_height)

    # count the number of frames
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)

    # calculate dusration of the video
    seconds = int(frames / fps)
    video_time = str(datetime.timedelta(seconds=seconds))

    print("duration in seconds:", seconds)
    print("video time:", video_time)
    print("video frame rate:", fps)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    output = cv2.VideoWriter("ass_" + file_path, fourcc, fps, size, 0)

    ret, frame = video.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    while video.isOpened():
        # Save the video
        output.write(frame)

        ret, frame = video.read()

        # check for successfulness of video.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    video.release()
    output.release()

    print("video save complete")
    end = time.time()
    seconds = end - start
    print("Time taken : {0} seconds".format(seconds))

    return "ass_" + file_path


# When the bot is ready, execution is from the section below
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


# This part will be executed when receive message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Save every attachments that is mp4 file
    for attachment in message.attachments:
        if attachment.filename.lower().endswith("mp4"):
            await attachment.save(attachment.filename)

            # Transfer the video into grayscale
            ass_video_path = await grayscale_video(attachment.filename)

            # Send the video file after processing
            await message.channel.send(file=discord.File(ass_video_path), content="")

            os.remove(ass_video_path)

        elif attachment.filename.lower().endswith("jpeg"):
            await attachment.save(attachment.filename)

            ass_img_path = await grayscale_pic(attachment.filename)

            await message.channel.send(file=discord.File(ass_img_path), content="")

            os.remove(ass_img_path)


client.run(TOKEN)
