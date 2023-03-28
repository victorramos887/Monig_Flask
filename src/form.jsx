import { Box, Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import Header from "../../components/Header";
import  SearchIcon from "@mui/icons-material/Search";
import urlLocal from "../../isHome";




var initialValues = {
    nome: "",
    cep: "",
    cidade: "",
    estado: "",
    logradouro: "",
    numero: "",
};

const userSchema = yup.object().shape({
    nome: yup.string().required("Obrigatório"),
    cep: yup.string().required("Obrigatório"),
    cidade: yup.string().required("Obrigatório"),
    estado: yup.string().required("Obrigatório"),
    logradouro: yup.string().required("Obrigatório"),
    numero: yup.string().required("Obrigatório"),
});


const Form = () => {
    const isNonMobile = useMediaQuery("(min-width:600px)");

    const handleCep = (valor, setFieldValue) => {

        const url = `https://viacep.com.br/ws/${valor.replace(/[^0-9]/g, '')}/json` 
        console.log(url)
        fetch(url , {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            })
            .then((response) => response.json())
            .then((data) => {
                if(data.erro) window.alert("CEP não encontrado");
                else{
                    setFieldValue('cidade', data.localidade)
                    setFieldValue('estado', data.uf)
                    setFieldValue('logradouro', data.logradouro)
                    .then(response => console.log(JSON.stringify(response)))
                }
            });

    }

    const handleFormSubmit = (values) => {
        const dataToSend = JSON.stringify(values);
        const urlCadastro = `${urlLocal}api/v1/cadastros/enderecos`

            fetch(urlCadastro , {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: dataToSend
            })
            .then(response => response.json())
            .then(response => console.log(JSON.stringify(response)))
    }

    return (
        <Box m="20px">
            <Header title="CADASTRO" subtitle="Cadastre um novo local"/>

        <Formik
          onSubmit={handleFormSubmit}
          initialValues={initialValues}
          validationSchema={userSchema}
          enablereinitialize={true}
          >
            {({ values, errors, touched, handleBlur, handleChange, handleSubmit, setFieldValue}) => (
                <form onSubmit={handleSubmit}>
                    <Box 
                     display="grid" 
                     gap="15px" 
                     gridTemplateColumns="repeat(16, minmax(0, 1fr))"
                     sx={{
                        "& > div": {gridColumn: isNonMobile ?undefined : "span 4"},
                     }}
                     >
                        <TextField 
                         fullWidth
                         gap="2px"
                         variant="filled"
                         type="text"
                         label="Nome do Local (Apelido)"
                         onBlur={handleBlur}
                         onChange={handleChange}
                         value={values.nome}
                         name="nome"
                         error={!!touched.nome && !!errors.nome}
                         helperText={touched.nome && errors.nome}
                         sx={{ gridColumn: "span 16"}}
                         />

                        <TextField 
                         gap="2px"
                         fullWidth
                         variant="filled"
                         type="text"
                         label="CEP"
                         onBlur={() => handleCep(values.cep, setFieldValue)}
                         onChange={handleChange}
                         value={values.cep}
                         name="cep"
                         error={!!touched.cep && !!errors.cep}
                         helperText={touched.cep && errors.cep}
                         sx={{ gridColumn: "span 5"}}
                         />

                         <Button 
                         onClick={() => handleCep(values.cep, setFieldValue)}
                         type="button"  
                         color="secondary" 
                         variant = "contained"
                         sx={{ gridColumn: "span 1", ml:"-10px", height:"56px", width:""}}
                         >
                          <SearchIcon />  
                        </Button>

                        <TextField 
                         fullWidth
                         variant="filled"
                         type="text"
                         label="Cidade"
                         onBlur={handleBlur}
                         onChange={handleChange}
                         value={values.cidade}
                         name="cidade"
                         error={!!touched.cidade && !!errors.cidade}
                         helperText={touched.cidade && errors.cidade}
                         sx={{ gridColumn: "span 8"}}
                         />
                         
                        <TextField 
                         fullWidth
                         variant="filled"
                         type="text"
                         label="UF"
                         onBlur={handleBlur}
                         onChange={handleChange}
                         value={values.estado}
                         name="estado"
                         error={!!touched.estado && !!errors.estado}
                         helperText={touched.estado && errors.estado}
                         sx={{ gridColumn: "span 2"}}
                         />

                         <TextField 
                         fullWidth
                         variant="filled"
                         type="text"
                         label="Logradouro"
                         onBlur={handleBlur}
                         onChange={handleChange}
                         value={values.logradouro}
                         name="logradouro"
                         error={!!touched.logradouro && !!errors.logradouro}
                         helperText={touched.logradouro && errors.logradouro}
                         sx={{ gridColumn: "span 10"}}
                         />

                         <TextField 
                         fullWidth
                         variant="filled"
                         type="text"
                         label="Número"
                         onBlur={handleBlur}
                         onChange={handleChange}
                         value={values.numero}
                         name="numero"
                         error={!!touched.numero && !!errors.numero}
                         helperText={touched.numero && errors.numero}
                         sx={{ gridColumn: "span 6"}}
                         />

                         
                    </Box>
                        <Box 
                        mt="20px"
                         display="flex" 
                         justifyContent="end" >
                        <Button type="submit"  color="secondary" variant = "contained">
                            Cadastrar Local
                        </Button>

                    </Box>
                    
                </form>
            )}

        </Formik>

        </Box>
    )

};

export default Form;