package com.example.music.src.music.entity;


import lombok.Getter;

import javax.persistence.*;

@Entity
@Getter
@Table(name = "MUSIC_GENRE")
public class MusicGenre {

    @Id @GeneratedValue
    @Column(name = "music_genre_id")
    private Long id; // table pk

    @ManyToOne
    @JoinColumn(name = "music_id")
    private Music music;

    @ManyToOne
    @JoinColumn(name = "genre_id")
    private Genre genre;
}
