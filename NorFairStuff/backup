      ldi r16,0x01
      ldi r17, 0xFF
      eor r0, r0
       ldi r19, 0x60
         eor r28, r28
              eor r29, r29

              ldi r30, 0xD7


      setup:
     in r24, 0x24
     ori r24, 0x20
     out 0x04,r24



      main:


     call  letterG

     call letterO

     call letterO

     call  pause
     call  pause
      rjmp main

      letterD:
              call turnon
              call pause
              call pause
              call pause
              call turnoff
              call pause
              call turnon
              call pause
              call turnoff
              call pause
              call turnon
              call pause
              call turnoff
              call pause
              call pause
              call pause
              ret
      letterU:
              call turnon
              call pause
              call turnoff
              call pause
              call turnon
              call pause
              call turnoff
              call pause
              call turnon
              call pause
              call pause
              call pause
              call turnoff
              call pause
              call pause
              call pause
              ret
      letterS:
              call turnon
              call pause
              call turnoff
              call pause

              call turnon
              call pause
              call turnoff
              call pause

              call turnon
              call pause
              call turnoff
              call pause

              rjmp letterS
      letterG:
           call turnon
           call pause
           call pause
           call pause
           call turnoff
           call pause
           call turnon
           call pause
           call pause
           call pause
           call turnoff
           call pause
           call turnon
           call pause
           call turnoff
           call pause
           call pause
           call pause
           ret

      letterO:
             call turnon
             call pause
             call pause
             call pause

           call turnoff
           call pause

           call turnon
           call pause
           call pause
           call pause

           call turnoff
           call pause

           call turnon
           call pause
           call pause
           call pause

           call turnoff
            call pause
            call pause
            call pause
           ret



     turnon:
     in r24, 0x05
     ori r24, 0x20
     out 0x05, r24

     ret

     resetval:
              eor r28, r28
              eor r29, r29
              ldi r30, 0xD7
              ret

     pause:
                 add r28, r16
                 adc r29, r0
                 adc r30, r0

                 brbs 0, resetval

                 rjmp pause






       turnoff:
     in r24, 0x05
     andi r24, 0xDF
     out 0x05, r24
     ret



