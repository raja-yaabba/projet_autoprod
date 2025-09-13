package com.example.demo.controller;

import com.example.demo.entity.UserEntity;
import com.example.demo.repository.UserRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
public class UserController {

    private final UserRepository userRepository;

    public UserController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // Page d’accueil : liste des utilisateurs
    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("users", userRepository.findAll());
        return "index";
    }

    // Ajouter un utilisateur
    @PostMapping("/add")
    public String add(@RequestParam("name") String name,
                      @RequestParam("email") String email) {
        UserEntity user = new UserEntity(name, email);
        userRepository.save(user);
        return "redirect:/";
    }

    // Supprimer un utilisateur
    @PostMapping("/delete/{id}")
    public String delete(@PathVariable("id") Long id) {
        userRepository.deleteById(id);
        return "redirect:/";
    }

    // Charger la page d’édition
    @GetMapping("/edit/{id}")
    public String editForm(@PathVariable("id") Long id, Model model) {
        UserEntity user = userRepository.findById(id).orElse(null);
        if (user == null) {
            return "redirect:/"; // évite erreur si id inexistant
        }
        model.addAttribute("user", user);
        return "edit";
    }

    // Sauvegarder la modification
    @PostMapping("/edit/{id}")
    public String edit(@PathVariable("id") Long id,
                       @RequestParam("name") String name,
                       @RequestParam("email") String email) {
        UserEntity user = userRepository.findById(id).orElse(null);
        if (user != null) {
            user.setName(name);
            user.setEmail(email);
            userRepository.save(user);
        }
        return "redirect:/";
    }
}
