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
