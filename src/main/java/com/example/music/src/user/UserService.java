package com.example.music.src.user;

import com.example.music.src.user.entity.User;
import com.example.music.src.user.model.LoginReq;
import com.example.music.src.user.model.LoginRes;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Transactional
@RequiredArgsConstructor
@Service
public class UserService {

    private final UserRepository userRepository;


    /**
     * login API
     * @param loginReq
     * @return
     */
    public LoginRes login(LoginReq loginReq){

        String encryptPwd;

        encryptPwd = loginReq.getPassword();

        Optional<User> byEmail = userRepository.findByEmail(loginReq.getEmail());
        if(byEmail.isEmpty())
            throw new IllegalArgumentException("유효하지 않은 이메일입니다.");


        // todo : db 검증
        // 1. email과 비번(암
        // 2. jwt 생
        // 비번 먼저
        userRepository.


        return new LoginRes("jwt");
    }
}
