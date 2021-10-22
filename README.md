
<h1 align="center">
    zoomrec	
</h1>

<h4 align="center">
	A all-in-one solution to automatically join and record Zoom meetings.
</h4>

<p align="center">
  <img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/kastldratza/zoomrec">
  <a href="https://github.com/aykborstelmann/zoomrec/actions/workflows/docker-publish.yml"><img src="https://github.com/aykborstelmann/zoomrec/actions/workflows/docker-publish.yml/badge.svg" alt="GitHub Workflow Status"></a>
</p>


---

- **Python3** - _Script to automatically join Zoom meetings and control FFmpeg_
- **FFmpeg** - _Triggered by python script to start/stop screen recording_
- **Docker** - _Headless VNC Container based on Ubuntu 20.04 with Xfce window manager and TigerVNC_

---

![Join a test meeting](doc/demo/join-meeting.gif)

---

**This project is a further development of https://github.com/kastldratza/zoomrec. 
Please also have a look at this repo and leave a star.**

## Installation

The entire mechanism runs in a Docker container. So all you need to do is install Docker and use the image from Registry.

### Requirements

- Docker - [https://docs.docker.com/get-docker/]()

### Docker Registry

Docker images are build and pushed automatically to [**Docker Hub**](https://hub.docker.com/repository/docker/kyatech/zoomrec) and [**GitHub Container Registry**](https://github.com/aykborstelmann/zoomrec/pkgs/container/zoomrec).

So you can choose and use one of them:
- ```ghcr.io/aykborstelmann/zoomrec:master```
- ```kyatech/zoomrec:latest```

*For my examples in this README I used* ```kyatech/zoomrec:latest```

---

## Usage
- Container saves recordings at **/home/zoomrec/recordings**
- The current directory is used to mount **recordings**-Folder, but can be changed if needed
  - Please check use of paths on different operating systems!
  - Please check permissions for used directory!
- Container stops when Python script is terminated
- Zoomrec uses a YML file with entries of Zoom meetings to record them
  - The csv can be passed as seen below (mount as volume or add to docker image)
- To "say" something after joining a meeting:
  - ***paplay*** (*pulseaudio-utils*) is used to play a sound to a specified microphone output, which is mapped to a microphone input at startup.
  - ***paplay*** is triggered and plays a random file from **/home/zoomrec/audio**
  - Nothing will be played if directory:
    - does not contain **.wav** files
    - is not mounted properly

### config.yml structure
* `compress` - if the recorded file should be compressed afterwards
(withour it is recorded with 0 compression as mkv file - 1 hour ~ 1GB)  
* `meetings` - array of meeting informations:  
  * **Must contain**:
    * `description` - description/name of the meeting used for filenmae
    * `day` - weekday on which this meeting occurs
    * `time` - time on which this meeting occurs
    * `duration` - duration the zoomrec will stay in meeting and record
  * **Either or**
    * `link` - link for the meeting
    * `id` and `password` - id and password of the meeting

**Example**
```yml
compress: true
meetings:
  - description: Meeting 1
    link: https://zoom.us/j/111111111111?pwd=741699
    day: monday
    time: '19:22'
    duration: 5
  - description: Meeting 2
    id: 111111111111
    password: 741699
    day: monday
    time: '0:05'
    duration: 5
```

### VNC
You can connect to zoomrec via vnc and see what is happening.

#### Connect (default)
Hostname | Port | Password
-------- | -------- | --------
localhost   | 5901   | zoomrec

### Preparation
To have access to the recordings, a volume is mounted, so you need to create a folder that container users can access.

**[ IMPORTANT ]**
#### Create folders and set permissions (on Host)
```
mkdir -p recordings
chown -R 1000:1000 recordings

mkdir -p audio
chown -R 1000:1000 audio
```

### Flags
#### Set timezone (default: Europe/Berlin)
```bash
docker run -d --restart unless-stopped \
  -e TZ=Europe/Berlin \
  -v $(pwd)/recordings:/home/zoomrec/recordings \
  -v $(pwd)/audio:/home/zoomrec/audio \
  -v $(pwd)/config.yml:/home/zoomrec/config.yml:ro \
  -p 5901:5901 \
kyatech/zoomrec:latest
```
#### Set debugging flag (default: False)
   - screenshot on error
   - record joining
```bash
docker run -d --restart unless-stopped \
  -e DEBUG=True \
  -v $(pwd)/recordings:/home/zoomrec/recordings \
  -v $(pwd)/audio:/home/zoomrec/audio \
  -v $(pwd)/config.yml:/home/zoomrec/config.yml.csv:ro \
  -p 5901:5901 \
kyatech/zoomrec:latest
```

### Windows / _cmd_

```cmd
docker run -d --restart unless-stopped \
  -v %cd%\recordings:/home/zoomrec/recordings \
  -v %cd%\audio:/home/zoomrec/audio \
  -v %cd%\config.yml:/home/zoomrec/config.yml:ro \
  -p 5901:5901 \
kyatech/zoomrec:latest
```

### Windows / _PowerShell_

```powershell
docker run -d --restart unless-stopped \
  -v ${PWD}/recordings:/home/zoomrec/recordings \
  -v ${PWD}/audio:/home/zoomrec/audio \
  -v ${PWD}/config.yml:/home/zoomrec/config.yml:ro \
  -p 5901:5901 \
kyatech/zoomrec:latest
```

### Linux / macOS

```bash
docker run -d --restart unless-stopped \
  -v $(pwd)/recordings:/home/zoomrec/recordings \
  -v $(pwd)/audio:/home/zoomrec/audio \
  -v $(pwd)/config.yml:/home/zoomrec/config.yml:ro \
  -p 5901:5901 \
kyatech/zoomrec:latest
```
---

## Supported actions
- [x] Show when the next meeting starts
- [x] _Join a Meeting_ from csv with id and password
- [x] Wrong error: _Invalid meeting ID_ / **Leave**
- [x] _Join with Computer Audio_
- [x] _Please wait for the host to start this meeting._
- [x] _Please wait, the meeting host will let you in soon._
- [x] _Enter Full Screen_
- [x] Switch to _Speaker View_
- [x] Continuously check: _This meeting is being recorded_ / **Continue**
- [x] Continuously check: _Hide Video Panel_
- [x] Continuously check: _This meeting has been ended by host_
- [x] Quit ffmpeg gracefully on abort
- [x] _Host is sharing poll results_
- [x] _This meeting is for authorized attendees only_ / **Leave meeting**
- [x] Play sound after joining a meeting
- [x] _Join a Meeting_ from csv with url

---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.