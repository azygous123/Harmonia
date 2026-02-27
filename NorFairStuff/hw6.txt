      ldi r16,0x01
      ldi r17, 0xFF
      eor r0, r0
       ldi r19, 0x60 ; decimal 100
         eor r28, r28
              eor r29, r29
              ;eor r30, r30
              ldi r30, 0xD7
      ;.equ _loopcounterTwo, r20
     ; ldi r20, 0x59
      ;.equ _loopcounterThree, r21
      ;ldi r21, 0x59; loop counter
      ;ldi r22, 0x01

      setup:
     in r24, 0x24
     ori r24, 0x20
     out 0x04,r24



      main:
      ;.equ _loopcounterOne, r19
     ; call letterD
      ;call letterU
      ;call letterS

     call  letterG

     call letterO

     call letterO
     ;call letterS
     call  pause
     call  pause
      rjmp main

      letterD:
              call turnon  ;turn on, wait 3 turn off pause 1
              call pause
              call pause
              call pause
              call turnoff
              call pause
              call turnon    ;turn on, wait 1 turn off pause 1
              call pause
              call turnoff
              call pause
              call turnon    ;turn on, wait 1 turn off pause 1
              call pause
              call turnoff
              call pause
              call pause
              call pause
              ret
      letterU:
              call turnon    ;turn on, wait 1 turn off pause 1
              call pause
              call turnoff
              call pause
              call turnon    ;turn on, wait 1 turn off pause 1
              call pause
              call turnoff
              call pause
              call turnon    ;turn on, wait 1 turn off pause 1
              call pause
              call pause
              call pause
              call turnoff
              call pause
              call pause
              call pause
              ret
      letterS:
              call turnon    ;turn on, wait 1 turn off pause 1
              call pause
              call turnoff
              call pause

              call turnon    ;turn on, wait 1 turn off pause 1
              call pause
              call turnoff
              call pause

              call turnon    ;turn on, wait 1 turn off pause 1
              call pause
              call turnoff
              call pause
              ;call pause
             ; call pause
              rjmp letterS
      letterG:
           call turnon  ;turn on, wait 3 turn off pause 1
           call pause
           call pause
           call pause
           call turnoff
           call pause
           call turnon   ;turn on, wait 3 turn off pause 1
           call pause
           call pause
           call pause
           call turnoff
           call pause
           call turnon    ;turn on, wait 1 turn off pause 1
           call pause
           call turnoff
           call pause
           call pause
           call pause
           ret

      letterO:
             call turnon  ;turn on, wait 3 turn off pause 1
             call pause
             call pause
             call pause

           call turnoff
           call pause

           call turnon   ;turn on, wait 3 turn off pause 1
           call pause
           call pause
           call pause

           call turnoff
           call pause

           call turnon   ;turn on, wait 3 turn off pause 1
           call pause
           call pause
           call pause

           call turnoff
            call pause
            call pause
            call pause
           ret

      ;longpause:
               ; call pause
               ; call pause
               ; call pause
                ;call pause
                ;call pause
                ;ret

     turnon:
     in r24, 0x05
     ori r24, 0x20  ; 0010 0000 andi turns off only the 6th bit
     out 0x05, r24
     ;nop
     ret

     resetval:
              eor r28, r28
              eor r29, r29
              ldi r30, 0xD7 ;D7 based of 16 million
              ret

     pause:
                 add r28, r16   ;256
                 adc r29, r0     ;256
                 adc r30, r0
                 ;adc r31,r0       ;256
                ; adc r31, r0
                 ;cp r30, r17
                 ;nop
                 ;nop
                 ;nop
                 ;nop
                 brbs 0, resetval
                  ;nop
                  ;nop
                  ;nop
                 rjmp pause






       turnoff:
     in r24, 0x05
     andi r24, 0xDF ; 1101 1111 andi turns off only the 6th bit
     out 0x05, r24
     ret



