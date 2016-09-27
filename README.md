# DNS Client 
----

* 사용법  
$ python dnsclient.py 8.8.8.8 www.naver.com  
(ENTER)  
...  
...  
...  


----
## 고민
* **DNS 메시지 구조에 헤더는 바이트, 비트 단위던데, 이걸 어떻게 파이썬으로 표현할 것인가?**  
>> bitarray, struct package로 해결 
* DNS Message Compression에 대해 고민 - 이것이 컴프레션이 됬는지 안됬는지를 어떻게 구분해야할까?  
* Message Compression pointer의 첫 2bits(11)을 어떻게 catch해낼 것인가?  
>> (바이트 형태로 구성되어있는 것을 하나하나 다 뜯어내야할 것인가?)  
>> (전부다 비트로 뜯을 순 없을 것 같고, 우선 이게 압축되었고 포인터의 위치를 정확히 파악할 수 있어야 한다.)  
* DNS Message Compression이 일어났는지 안 일어났는지를 어떻게 파악할 지?  
>> msg를 바이트 단위로 읽어들이면서 compression pointer의 특징인 상위 2bits가 1인 것을 파악 후 두바이트로 묶어 pointer의 reference를 해석  
* Resource Record는 사이즈가 계속 변하기때문에, 1~2 바이트 단위로 루프를 돌면서 RR을 파싱할 수 밖에 없는 것인가?  
>> Resource data필드는 Resource data length로 길이를 파악이 가능하겠지만 name 필드는 답이 없는 것 같다.  그런데 이전 Resource Record의 Resource data를 지칭하는 것 같긴한데,,