package com.example.music.src.user;

import static com.example.music.common.response.BaseResponseStatus.*;

import com.example.music.common.exceptions.BaseException;
import com.example.music.src.user.entity.User;
import com.example.music.src.user.model.LoginReq;
import com.example.music.src.user.model.LoginRes;
import com.example.music.src.utils.SHA256;
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

        User user;
        // todo : db 검증
        String encryptPwd;
        encryptPwd = new SHA256().encrypt(loginReq.getPassword());

        user = userRepository.findByEmail(loginReq.getEmail())
                .orElseThrow(()-> new BaseException(USER_INVALID_EMAIL));

        if(!user.getPassword().equals(encryptPwd)){
            throw new BaseException(USER_INVALID_PASSWORD);
        }

        // todo : jwt 생성



        return new LoginRes("jwt");
    }
}
