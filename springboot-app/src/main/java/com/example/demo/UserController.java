package com.example.demo;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class UserController {

    private final UserRepository userRepository;

    public UserController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // Page d’accueil
    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("users", userRepository.findAll());
        return "index";
    }

    // Ajouter un utilisateur
    @PostMapping("/add")
    public String add(@RequestParam String name, @RequestParam String email) {
        UserEntity user = new UserEntity();
        user.setName(name);
        user.setEmail(email);
        userRepository.save(user);
        return "redirect:/";
    }

    // Supprimer un utilisateur
    @PostMapping("/delete/{id}")
    public String delete(@PathVariable Long id) {
        userRepository.deleteById(id);
        return "redirect:/";
    }

    // Modifier un utilisateur
    @GetMapping("/edit/{id}")
    public String editForm(@PathVariable Long id, Model model) {
        UserEntity user = userRepository.findById(id).orElse(null);
        model.addAttribute("user", user);
        return "edit";
    }

    @PostMapping("/edit/{id}")
    public String edit(@PathVariable Long id,
                       @RequestParam String name,
                       @RequestParam String email) {
        UserEntity user = userRepository.findById(id).orElse(null);
        if (user != null) {
            user.setName(name);
            user.setEmail(email);
            userRepository.save(user);
        }
        return "redirect:/";
    }
}
