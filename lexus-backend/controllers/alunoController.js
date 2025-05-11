const db = require('../db');
const bcrypt = require('bcrypt');

exports.cadastrar = async (req, res) => {
  const { nome, email, senha } = req.body;
  const hashed = await bcrypt.hash(senha, 10);
  const query = 'INSERT INTO alunos (nome, email, senha) VALUES (?, ?, ?)';

  db.query(query, [nome, email, hashed], (err) => {
    if (err) return res.status(500).json({ erro: err });
    res.status(201).json({ mensagem: 'Aluno cadastrado!' });
  });
};

exports.login = (req, res) => {
  const { email, senha } = req.body;
  const query = 'SELECT * FROM alunos WHERE email = ?';

  db.query(query, [email], async (err, results) => {
    if (err) return res.status(500).json({ erro: err });
    if (results.length === 0) return res.status(401).json({ erro: 'Usuário não encontrado' });

    const aluno = results[0];
    const isMatch = await bcrypt.compare(senha, aluno.senha);
    if (!isMatch) return res.status(401).json({ erro: 'Senha inválida' });

    res.json({ mensagem: 'Login bem-sucedido', aluno });
  });
};
 