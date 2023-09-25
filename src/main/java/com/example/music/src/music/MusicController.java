package com.example.music.src.music;

import com.example.music.src.library.LibraryService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Slf4j
@Controller
@RequestMapping("/musics")
@RequiredArgsConstructor
public class MusicController {

    private final LibraryService libraryService;

}
