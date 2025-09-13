package com.example.demo;

import com.example.demo.entity.UserEntity;
import com.example.demo.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        userRepository.deleteAll(); // nettoie la base avant chaque test
    }

    @Test
    void testIndexPageLoads() throws Exception {
        mockMvc.perform(get("/"))
                .andExpect(status().isOk())
                .andExpect(view().name("index"))
                .andExpect(model().attributeExists("users"));
    }

    @Test
    void testAddUser() throws Exception {
        mockMvc.perform(post("/add")
                .contentType(MediaType.APPLICATION_FORM_URLENCODED)
                .param("name", "Alice")
                .param("email", "alice@example.com"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/"));

        assertThat(userRepository.findAll()).extracting(UserEntity::getName).contains("Alice");
    }

    @Test
    void testDeleteUser() throws Exception {
        UserEntity user = userRepository.save(new UserEntity("Bob", "bob@example.com"));

        mockMvc.perform(post("/delete/" + user.getId()))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/"));

        assertThat(userRepository.findById(user.getId())).isEmpty();
    }

    @Test
    void testEditUser() throws Exception {
        UserEntity user = userRepository.save(new UserEntity("Charlie", "charlie@example.com"));

        mockMvc.perform(post("/edit/" + user.getId())
                .contentType(MediaType.APPLICATION_FORM_URLENCODED)
                .param("name", "Charles")
                .param("email", "charles@example.com"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/"));

        UserEntity updated = userRepository.findById(user.getId()).orElseThrow();
        assertThat(updated.getName()).isEqualTo("Charles");
        assertThat(updated.getEmail()).isEqualTo("charles@example.com");
    }
}
