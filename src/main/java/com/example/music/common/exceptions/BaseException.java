package com.example.music.common.exceptions;

import com.example.music.common.response.BaseResponseStatus;
import lombok.Getter;
import lombok.Setter;

@Getter @Setter
public class BaseException extends RuntimeException{

    private BaseResponseStatus status;


    public BaseException(BaseResponseStatus status) {
        super(status.getMessage());
        this.status = status;
    }

}
