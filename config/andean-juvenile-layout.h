ZMK_COMBO(tab_combo, &kp TAB, 11 13, ALL, 50)
ZMK_COMBO(mov_combo, &mo 3, 12 13, ALL, 50)
ZMK_COMBO(opt_combo, &kp LALT, 3 4, ALL, 50)
ZMK_COMBO(ret_combo, &kp RET, 16 18, ALL, 50)
ZMK_COMBO(sft_combo, &sk LSHIFT, 16 17, ALL, 50)
ZMK_COMBO(caps_combo, &caps_word, 16 17 18, ALL, 50)
ZMK_LAYER(BASE,
 &kp Q           &kp W           &kp E           &kp R           &kp T           &kp Y           &kp U           &kp I           &kp O           &kp P          
 &kp A           &kp S           &kp D           &hml LCTRL F    &kp G           &kp H           &hmr RCTRL J    &kp K           &kp L           &colonsemi     
 &kp Z           &kp X           &kp C           &kp V           &kp B           &kp N           &kp M           &kp COMMA       &kp DOT         &kp SLASH      
 &none           &kp LCMD        &mo 1           &hmr RSHIFT SPACE &sym_layer6     &none          )
ZMK_LAYER(NUM,
 &kp EXCL        &kp AT          &kp HASH        &kp DLLR        &kp PERCENT     &kp CARET       &kp N7          &kp N8          &kp N9          &degree_symbol 
 &kp DQT         &kp AMPS        &kp STAR        &kp UNDER       &kp N0          &kp PLUS        &kp N4          &kp N5          &kp N6          &kp SQT        
 &multiplication_sign &division_sign  &kp EQUAL       &kp MINUS       &kp DOT         &none           &kp N1          &kp N2          &kp N3          &kp SLASH      
 &none           &kp LCMD        &trans          &hmr RSHIFT SPACE &none           &none          )
ZMK_LAYER(SYM,
 &left_double_quote &right_double_quote &left_single_quote &right_single_quote &double_prime   &micro          &ohm            &none           &en_dash        &none          
 &kp LBKT        &kp RBKT        &kp LPAR        &kp RPAR        &prime          &kp TILDE       &kp MINUS       &kp EQUAL       &em_dash        &kp PIPE       
 &kp LT          &kp GT          &kp LBRC        &kp RBRC        &kp GRAVE       &none           &none           &none           &none           &kp BACKSLASH  
 &none           &mo 9           &none           &hmr RSHIFT SPACE &trans          &none          )
ZMK_LAYER(MOV,
 &none           &none           &kp LG(LBRC)    &kp LG(RBRC)    &none           &kp ESC         &kp PGUP        &kp UP          &kp PGDN        &none          
 &none           &none           &kp LG(B)       &kp LG(F)       &ispell_word    &kp BSPC        &kp LEFT        &kp DOWN        &kp RIGHT       &kp LG(M)      
 &none           &none           &none           &none           &none           &kp DEL         &kp HOME        &none           &kp END         &none          
 &none           &kp LCMD        &mo 4           &hmr RSHIFT SPACE &none           &none          )
ZMK_LAYER(NAV,
 &none           &none           &none           &none           &none           &none           &kp LC(LG(B))   &kp LC(LG(F))   &none           &none          
 &none           &none           &none           &none           &none           &none           &kp LG(LBRC)    &kp LG(RBRC)    &kp LG(B)       &kp LG(F)      
 &none           &none           &none           &none           &none           &none           &kp LA(LG(LEFT)) &kp LA(LG(RIGHT)) &none           &none          
 &none           &kp LCMD        &trans          &hmr RSHIFT SPACE &none           &none          )
ZMK_LAYER(ACC,
 &none           &umlat          &accented_e     &none           &none           &none           &accented_u     &accented_i     &accented_o     &none          
 &accented_a     &none           &none           &none           &none           &none           &none           &none           &none           &none          
 &none           &none           &none           &none           &none           &tilde_n        &none           &none           &upsidedown_bang &upsidedown_question
 &none           &none           &none           &none           &none           &none          )
ZMK_LAYER(layer_6,
 &none       &none       &none       &none       &none       &none       &none       &none       &none       &bootloader
 &none       &kp F       &kp R       &kp E       &kp E       &none       &none       &none       &none       &none      
 &none       &none       &none       &none       &none       &none       &none       &none       &none       &none      
 &none       &none       &none       &none       &none       &none      )
ZMK_LAYER(layer_7,
 &none &none &none &none &none &none &none &none &none &none
 &none &none &none &none &none &none &none &none &none &none
 &none &none &none &none &none &none &none &none &none &none
 &none &none &none &none &none &none)
ZMK_LAYER(BOX,
 &none           &none           &box_upperleft  &box_upperright &none           &none           &none           &none           &none           &none          
 &box_horizontal &box_vertical   &box_lowerleft  &box_lowerright &none           &tog 8          &none           &none           &none           &none          
 &box_middle     &box_middlebottom &box_middletop  &box_middleright &box_middleleft &none           &none           &none           &none           &none          
 &none           &kp LCMD        &none           &none           &none           &none          )
ZMK_LAYER(FN,
 &kp ESC        &kp F1         &kp F2         &kp F3         &kp F4         &kp F5         &kp F6         &kp F7         &kp F8         &kp F9        
 &none          &flip_buffer   &kp LC(LG(N0)) &kp LC(LG(N1)) &none          &clear_shell   &kp LC(LG(N2)) &kp LC(LG(N3)) &kp LG(O)      &none         
 &kp F10        &kp F11        &kp F12        &kp F13        &kp F14        &kp F15        &kp F16        &kp F17        &kp F18        &kp LG(LS(N4))
 &none          &trans         &none          &none          &trans         &none         )
