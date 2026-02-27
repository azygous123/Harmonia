
ldi r16, 0x02
eor r17, r17
mov r17, r16

eor r1, r1
     com r1

       eor r19, r19
       eor r18, r18


Multiply:




       add r18, r16
       add r17, r1
       brbc 1,  Multiply

            ;2x = r19
       add r19, r16
       add r19, r16

            eor r17, r17

            add r17, r18
            add r17, r19
            com r17
            neg r17
Sink:
rjmp Sink






