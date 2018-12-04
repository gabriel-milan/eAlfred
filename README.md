# 
![Image](https://raw.githubusercontent.com/gabriel-milan/eAlfred/master/server/static/images/eAlfred_Text_Black.png)

Hi! I'm e-Alfred, your electronic butler. You can add sensors and actuators to my Arduino and be sure that you'll be able to control them using my web interface.

# Setup

### Clone the repository
First you need to clone this repository:
```
git clone https://github.com/gabriel-milan/eAlfred.git
```
### Install requirements
Then, go to the "server" folder and run
```
pip3 install -r requirements.txt
```
### Run web server
If everything goes okay, you'll be able to run the server with
```
./run.sh
```
or
```
python3 routes.py
```

# Message protocol

e-Alfred works with a very simple message exchange protocol, as follows:

### First step: Server sends POST request with JSON body to Arduino
Message example:
```
{
	"request_type" : 0,
	"port_type" : 0,
	"port_number" : 7,
	"value" : 53
}
```
where
* _request_type_ is the type of action Arduino will perform (0 for reading, 1 for writing and 2 for PWM writing);
* _port_type_ is the type of the Arduino port chosen (0 for analog, 1 for digital);
* _port_number_ is the number of the Arduino port chosen (depends on the board model);
* _value_ is the value for writing data (useless if _request_type_ = 0).

### Second step: Server gets a JSON response from Arduino
Message example:
```
{
	"data" : 73,
}
```
where
* _data_ is the data written from the port, when _request_type_ = 0. In any other case, it just doesn't matter.

## How Arduino shall interpret the message
| request_type | port_type | port_number | value | Arduino commands                                       |
|:------------:|-----------|-------------|-------|--------------------------------------------------------|
|       0      | 0         | X           | y     | ``` pinMode("A"+X, INPUT); analogRead("A"+X); ```      |
|       0      | 1         | X           | y     | ``` pinMode(X, INPUT); digitalRead(X); ```             |
|       1      | 0         | X           | y     | ``` pinMode("A"+X, OUTPUT); analogWrite("A"+X, y); ``` |
|       1      | 1         | X           | y     | ``` pinMode(X, OUTPUT); digitalWrite(X, value); ```    |
|       2      | 0         | X           | y     | ===== THIS WON'T HAPPEN =====                          |
|       2      | 1         | X           | y     | ``` pinMode(X, OUTPUT); digitalWrite(X, value); ```    |