package com.example.music.src.library.model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter @Setter
@NoArgsConstructor
@AllArgsConstructor
public class PatchMusicReq { // 음악 정보 수정 요청

    private String music_name;
    private boolean visible; // 공개 여부 -> true(1) 공개 | false(0) 비공개
}
