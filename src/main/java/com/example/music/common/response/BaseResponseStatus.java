package com.example.music.common.response;

import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
public enum BaseResponseStatus {

    /**
     * 200 : 요청 성공
     */
    SUCCESS(true,HttpStatus.OK.value(), "요청에 성공하였습니다."),


    /**
     * 400 : Request, Response 오류
     */
    USER_INVALID_EMAIL(false,HttpStatus.BAD_REQUEST.value(), "이메일 정보가 올바르지 않습니다."),
    USER_INVALID_PASSWORD(false,HttpStatus.BAD_REQUEST.value(), "비밀번호 정보가 올바르지 않습니다.");


    private final boolean isSuccess;
    private final int code;
    private final String message;

    private BaseResponseStatus(boolean isSuccess, int code, String message) {
        this.isSuccess = isSuccess;
        this.code = code;
        this.message = message;
    }
}
