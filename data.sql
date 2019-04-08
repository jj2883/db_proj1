
CREATE TABLE Record(
player_id INTEGER,
game_id INTEGER,
PRIMARY KEY(player_id, game_id),
FOREIGN KEY(player_id) REFERENCES PLAYER,
FOREIGN KEY(game_id) REFERENCES GAME
);


INSERT INTO TEAM VALUES(1, 'Bulls', 'East');
INSERT INTO TEAM VALUES(2, 'Nets', 'East');
INSERT INTO TEAM VALUES(3, 'Pistons', 'East');
INSERT INTO TEAM VALUES(4, 'Warriors', 'West');
INSERT INTO TEAM VALUES(5, 'Spurs', 'West');




INSERT INTO PLAYER VALUES(11, 'James', 'Harden', '1985-02-08',500,800);
INSERT INTO PLAYER VALUES(12, 'Xiao', 'Meng', '1990-05-08',200,500);
INSERT INTO PLAYER VALUES(13, 'Dean', 'McGill', '1980-02-08',300,1000);
INSERT INTO PLAYER VALUES(14, 'Chris', 'Bosh', '1978-03-17',900,1200);
INSERT INTO PLAYER VALUES(15, 'Michale', 'Jordan', '1975-08-08',600,800);



INSERT INTO COACH VALUES(21, 'Karl', 'Stinger', '1960-05-22', 400,1200);
INSERT INTO COACH VALUES(22, 'Steve', 'Helios', '1956-10-12', 700,1400);
INSERT INTO COACH VALUES(23, 'Ray', 'Raven', '1975-04-22', 600, 1100);
INSERT INTO COACH VALUES(24, 'Marvin', 'Steinson', '1945-04-29', 1000,1500);
INSERT INTO COACH VALUES(25, 'Magic', 'Raelis', '1980-04-21', 200,500);



INSERT INTO GAME VALUES(31, 1,2,55,89);
INSERT INTO GAME VALUES(32,2,5,141,89);
INSERT INTO GAME VALUES(33,3,4,120,77);
INSERT INTO GAME VALUES(34,4,2,88,62);
INSERT INTO GAME VALUES(25,5,1,70,102);









INSERT INTO STATLINE VALUES(31,25,12,5,8,10,6,8,2,5,30,5,2,0,45,11);
INSERT INTO STATLINE VALUES(31,30,12,10,3,2,10,6,1,1,35,2,1,4,1,28,12);
INSERT INTO STATLINE VALUES(32,10,12,5,9,12,4,6,1,2,15,2,1,4,1,28,12);
INSERT INTO STATLINE VALUES(32,50,20,12,12,5,7,9,1,5,30,2,1,0,1,30,15);
INSERT INTO STATLINE VALUES(33,20,30,13,15,27,4,4,6,3,30,4,2,1,0,80,13);
INSERT INTO STATLINE VALUES(33,25,12,5,8,10,6,8,2,5,30,5,2,0,45,14);
INSERT INTO STATLINE VALUES(34,10,12,6,15,21,6,8,3,2,22,9,2,3,0,30,14);
INSERT INTO STATLINE VALUES(34,50,12,10,15,7,10,7,1,3,15,2,1,6,0,22,12);
INSERT INTO STATLINE VALUES(35,15,2,33,0,2,2,4,1,1,10,1,0,0,0,15,15);
INSERT INTO STATLINE VALUES(35,60,21,15,24,10,20,13,6,1,20,2,5,0,0,50,11);



INSERT INTO Coaches VALUES(41,1,'2018-04-12','2020-04-12',1000000);
INSERT INTO Coaches VALUES(42,2,'2018-04-14','2019-04-13',2000000);
INSERT INTO Coaches VALUES(43,3,'2018-04-18','2019-04-17',500000);
INSERT INTO Coaches VALUES(44,4,'2018-04-10','2019-04-09',1200000);
INSERT INTO Coaches VALUES(45,5,'2018-04-08','2019-04-07',1100000);






INSERT INTO Play VALUES(1,2,31);
INSERT INTO Play VALUES(2,5,32);
INSERT INTO Play VALUES(3,4,33);
INSERT INTO Play VALUES(4,2,34);
INSERT INTO Play VALUES(5,1,35);




INSERT INTO Play_for VALUES(11,1,'2018-04-12','2020-04-12',5000000);
INSERT INTO Play_for VALUES(12,2,'2018-04-13','2019-04-11',4000000);
INSERT INTO Play_for VALUES(13,3,'2018-04-11','2019-04-10',2500000);
INSERT INTO Play_for VALUES(14,4,'2018-04-12','2019-04-11',6000000);
INSERT INTO Play_for VALUES(15,5,'2018-04-13','2020-04-12',4300000);




INSERT INTO Record VALUES(11,31);
INSERT INTO Record VALUES(12,31);
INSERT INTO Record VALUES(12,32);
INSERT INTO Record VALUES(15,32);
INSERT INTO Record VALUES(13,33);
INSERT INTO Record VALUES(14,33);
INSERT INTO Record VALUES(14,34);
INSERT INTO Record VALUES(12,34);
INSERT INTO Record VALUES(15,35);
INSERT INTO Record VALUES(11,35);


