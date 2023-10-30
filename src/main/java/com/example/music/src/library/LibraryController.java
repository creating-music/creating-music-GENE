package com.example.music.src.library;

import com.example.music.src.library.model.PatchMusicReq;
import com.example.music.src.playlist.PlayListService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@Slf4j
@Controller
@RequestMapping("/library")
@RequiredArgsConstructor
public class LibraryController {

    private final LibraryService libraryService;

//
//    /**
//     * API 11 라이브러이에 자신이 만든 음악 추가
//     */
//
////    @GetMapping("/")
////    public String addMusicToLibrary(@PathVariable())
//
//
//    /**
//     * API 12 자신이 만든 특정 음악 정보 수정
//     */
//    @PatchMapping("/musics/{musicId}")
//    public String editMusicInfo(@PathVariable("musicId") Long musicId, @RequestBody PatchMusicReq patchMusicReq){
//        // todo : 사용자 jwt 검증
//
//
//        // Todo: 수정된 음악 정보 return
//        return "음악 수정 완료";
//    }
//
//    /**
//     * API 13 자신이 만든 특정 음악 정보 삭제
//     */
//    @DeleteMapping ("/musics/{musicId}")
//    public String deleteMusicInfo(@PathVariable("musicId") Long musicId){
//        // todo : 사용자 jwt 검증
//
//
//
//        return "음악 삭제 완료";
//    }
//
//
//    /**
//     * API 14 플레이 리스트 생성
//    */
//    @PostMapping("/musics/playlists")
//    public String createPlaylist(){
//        // todo : 사용자 jwt 검증
//
//
//        // todo 생성한 플레이 리스트 고유 번호 return
//        return "플레이 리스트 생성 완료";
//    }




}
