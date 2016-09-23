# DNS Client 
----


## get\_ip\_addr(hostname) return: ip\_addr
----  
### 로직  
> 1. local DNS ip주소를 얻는다.  
> 2. DNS 요청 포맷에 맞게 메시지 구성한다.  
> 3. local DNS에게 hostname에 대한 ip주소를 물어본다.  
> 4. local DNS에 ip주소가 캐싱되있다면 ip 주소를 리턴하고 끝난다.  
캐싱되어있지 않다면, root DNS 서버에게 hostname의 ip를 물어야하므로 root DNS의 주소를 얻는다.  
> 5. root DNS에게 hostname의 ip를 요청한다.  
> 6. root DNS로 부터 TLD DNS의ip를 얻는다.  
> 7. TLD DNS에게 hostname의 ip를 요청한다.  
> 8. TLD DNS로부터 hostname의 authoritative DNS서버의 ip를 얻는다.  
> 9. authoritative DNS서버에게 hostname의 ip주소를 묻는다.  
> 10. hostname의 ip주소를 리턴한다.  

----
## dns\_message\_parser도 필요할 듯


----
## 고민
* **DNS 메시지 구조에 헤더는 바이트, 비트 단위던데, 이걸 어떻게 파이썬으로 표현할 것인가?**  
* 플래그의 구조 및 성격을 좀더 이해할 필요가 있는 것 같다.  
