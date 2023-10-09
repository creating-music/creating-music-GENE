package com.example.music.src.music.entity;

import lombok.Getter;

import javax.persistence.*;

@Getter
@Entity
@Table(name = "MOOD")
public class Mood {

    @Id @GeneratedValue
    @Column(name = "mood_id")
    private Long id;

    @Column(nullable = false)
    private String name;

}
