const express = require('express');
const bcrypt = require('bcrypt');
const db = require('../db');
const router = express.Router();

// Rota de cadastro de professor
router.post('/cadastro', async (req, res) => {
  const { nome, email, senha, confirmarSenha } = req.body;

  if (!nome || !email || !senha || !confirmarSenha) {
    return res.status(400).json({ erro: "Preencha todos os campos." });
  }

  if (senha !== confirmarSenha) {
    return res.status(400).json({ erro: "As senhas não coincidem." });
  }

  try {
    const senhaHash = await bcrypt.hash(senha, 10);
    const sql = 'INSERT INTO professores (nome, email, senha) VALUES (?, ?, ?)';
    
    db.query(sql, [nome, email, senhaHash], (err, result) => {
      if (err) {
        if (err.code === 'ER_DUP_ENTRY') {
          return res.status(409).json({ erro: 'Email já cadastrado.' });
        }
        return res.status(500).json({ erro: 'Erro ao cadastrar professor.' });
      }

      res.status(201).json({ mensagem: 'Professor cadastrado com sucesso!' });
    });
  } catch (error) {
    res.status(500).json({ erro: 'Erro interno do servidor.' });
  }
});

// Rota de login de professor
router.post('/login', (req, res) => {
  const { email, senha } = req.body;

  if (!email || !senha) {
    return res.status(400).json({ erro: "Preencha todos os campos." });
  }

  const sql = 'SELECT * FROM professores WHERE email = ?';
  db.query(sql, [email], async (err, results) => {
    if (err || results.length === 0) {
      return res.status(401).json({ erro: 'Professor não encontrado.' });
    }

    const professor = results[0];
    const senhaConfere = await bcrypt.compare(senha, professor.senha);

    if (!senhaConfere) {
      return res.status(401).json({ erro: 'Senha incorreta.' });
    }

    res.status(200).json({ mensagem: 'Login realizado com sucesso!' });
  });
});

module.exports = router;
