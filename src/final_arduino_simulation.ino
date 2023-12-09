unsigned char ans_from_yolo;
unsigned char curr_light = 1;
unsigned char blink_cnt = 40;

int cnt = 0;
unsigned char mask = 0x03;

void flush_read_buffer() {
  while(Serial.available() >= 1) {
    Serial.read();
  }
}

int _blink() {
  return --blink_cnt;
}

void _toggle_light() {
  curr_light = curr_light ^ 0x01;
}

void setup() {
  // put your setup code here, to run once:
  int i = 0;
  for(i = 2; i < 9; i++) {
    pinMode(i, OUTPUT);
  }
  // pin for check traffic light
  pinMode(13, OUTPUT); // GREEN
  pinMode(12, OUTPUT); // RED
  pinMode(11, OUTPUT); // YELLO instead of blinking
  digitalWrite(13, HIGH);
  Serial.begin(9600);
  curr_light = 1;
  blink_cnt = 40;
}

void turnOn(char direction) {
  int start_var = (direction == '1') ? 9 : 2;
  int inc = (direction == '1') ? -1 : 1;

  while (start_var < 10 and start_var > 1) {
    digitalWrite(start_var, HIGH);
    start_var += inc;
    delay(50);
  }
}

void turnOff() {
  for(int i = 2; i < 10; i++) {
    digitalWrite(i, LOW);
  }
}

void changeTrafficLight() {
  digitalWrite(13, curr_light);
  digitalWrite(12, !curr_light);
}

void loop() {
  Serial.flush();
  
  if(curr_light > 0 && blink_cnt < 20) {
  
  
    digitalWrite(11, HIGH);
    if(Serial.available() >= 1) {
      ans_from_yolo = (char)Serial.read();
      Serial.flush();
      
      if(ans_from_yolo != '0') {
        turnOn(ans_from_yolo);
      } else {
        turnOff();
      }
    }
  }
  else {
    digitalWrite(11, LOW);
    turnOff();
  }

  int light_cnt = _blink();
  
  if(light_cnt == 0) {
    _toggle_light();
    changeTrafficLight();
    blink_cnt = 40;
  }
  flush_read_buffer();
  delay(1000);
}
