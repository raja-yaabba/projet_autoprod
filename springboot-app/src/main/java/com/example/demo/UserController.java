package com.example.springbootapp.controller;

import com.example.springbootapp.model.User;
import com.example.springbootapp.repository.UserRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class UserController {

    private final UserRepository userRepository;

    public UserController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("users", userRepository.findAll());
        return "index"; // templates/index.html
    }

    @PostMapping("/add")
    public String addUser(@RequestParam String name, @RequestParam String email) {
        userRepository.save(new User(name, email));
        return "redirect:/";
    }

    @PostMapping("/delete/{id}")
    public String deleteUser(@PathVariable Long id) {
        userRepository.deleteById(id);
        return "redirect:/";
    }
}
