package com.example.music.src.music.entity;

import com.example.music.src.playlist.entity.PlayList;
import lombok.Getter;
import org.springframework.web.bind.annotation.CrossOrigin;

import javax.persistence.*;

@Getter
@Entity
@Table(name = "MUSIC_PLAYLIST")
public class MusicPlaylist {

    @Id @GeneratedValue
    @Column(name = "music_playlist_id")
    private Long id;

    @ManyToOne
    @JoinColumn(name = "playlist_id")
    private PlayList playList;

    @ManyToOne
    @JoinColumn(name = "music_id")
    private Music music;
}
