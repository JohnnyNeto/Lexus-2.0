const express = require('express');
const cors = require('cors');
const app = express();
const alunoRoutes = require('./routes/alunos');
const professorRoutes = require('./routes/professores');

app.use(cors());
app.use(express.json());

app.use('/api/alunos', alunoRoutes);
app.use('/api/professores', professorRoutes);

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
