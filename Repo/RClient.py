ó
jXc           @   s   d  d l  Z  d  d l m Z d  d l m Z e   Z d e f d     YZ e d k r e   Z e d d  j	   Z
 e j e
 d	  GHn  d S(
   iÿÿÿÿN(   t   md5(   t   dbapit   RClientc           B   s&   e  Z d    Z d d  Z d   Z RS(   c         C   s£   t  j   } | d } | d } | |  _ t |  j   |  _ d |  _ d |  _ i |  j d 6|  j d 6|  j d 6|  j d 6|  _ i d	 d
 6d d 6d d 6|  _	 d  S(   Nt   rk_usert   rk_pwdt   72358t    a6b010fff6d247669c4b4bde98673709t   usernamet   passwordt   softidt   softkeys
   Keep-Alivet
   Connections   100-continuet   Expectt   bens
   User-Agent(
   R   t   GetCodeSettingR   R    t	   hexdigestR   t   soft_idt   soft_keyt   base_paramst   headers(   t   selft   rkR   R   (    (    s-   /home/zunyun/workspace/TaskConsole/RClient.pyt   __init__
   s     

			


i<   c         C   se   i | d 6| d 6} | j  |  j  i d | f d 6} t j d d | d | d |  j } | j   S(	   s@   
        im: å¾çå­è
        im_type: é¢ç®ç±»å
        t   typeidt   timeouts   a.jpgt   images"   http://api.ruokuai.com/create.jsont   datat   filesR   (   t   updateR   t   requestst   postR   t   json(   R   t   imt   im_typeR   t   paramsR   t   r(    (    s-   /home/zunyun/workspace/TaskConsole/RClient.pyt	   rk_create!   s    
$c         C   sE   i | d 6} | j  |  j  t j d d | d |  j } | j   S(   s)   
        im_id:æ¥éé¢ç®çID
        t   ids'   http://api.ruokuai.com/reporterror.jsonR   R   (   R   R   R   R   R   R   (   R   t   im_idR"   R#   (    (    s-   /home/zunyun/workspace/TaskConsole/RClient.pyt   rk_report_error/   s
    
(   t   __name__t
   __module__R   R$   R'   (    (    (    s-   /home/zunyun/workspace/TaskConsole/RClient.pyR      s   	t   __main__s/   /home/zunyun/PycharmProjects/untitled3/home.jpgt   rbià  (   R   t   hashlibR    R   t   objectR   R(   t   rct   opent   readR    R$   (    (    (    s-   /home/zunyun/workspace/TaskConsole/RClient.pyt   <module>   s   	3	