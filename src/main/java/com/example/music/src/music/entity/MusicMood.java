package com.example.music.src.music.entity;

import lombok.Getter;

import javax.persistence.*;

@Getter
@Entity
@Table(name = "MUSIC_MOOD")
public class MusicMood {

    @Id @GeneratedValue
    private Long id;

    @ManyToOne
    @JoinColumn(name = "genre_id")
    private Genre genre;

    @ManyToOne
    @JoinColumn(name = "mood_id")
    private Mood mood;


}
