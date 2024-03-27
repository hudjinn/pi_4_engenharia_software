package com.sysadm.sysadm;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/api") 
public class SysadmApplication {

    @PostMapping("/login")
    public ResponseEntity<String> fazerLogin(@RequestBody Login loginDados) {
        // implementar a lógica de login
        return ResponseEntity.ok().build();
    }

    @PostMapping("/createacc")
    public ResponseEntity<String> registrarUsuario(@RequestBody CreateAcc registroDados) {
        // implementar a lógica de registro
        return ResponseEntity.ok().build();
    }

    @PostMapping("/alteracc")
    public ResponseEntity<String> alterarSenha(@RequestBody AlterAcc alteracaoSenhaDados) {
        // implementar a lógica de alteração de senha
        return ResponseEntity.ok().build();
    }

	// Inserir rota para CRUD
}
