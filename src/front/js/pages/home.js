import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";

export const Home = () => {
	const { store, actions } = useContext(Context);
	const [user, setUser] = useState({
		email: "",
		name: "",
		password: ""
	})

	const handleChange = (event) => {
		setUser({
			...user,
			[event.target.name]: event.target.value
		})

	}

	const saveUser = async () => {
		let response = await actions.createUser(user)

		if (response) {
			alert("congratulation user saved")
		} else {
			alert("i am sorrillo")
		}
	}


	return (
		<div className="container">
			<div className="row justify-content-center">
				<div className="col-12 col-md-6">
					<form >
						<h1>Guardar usuario</h1>
						<div className="form-group">
							<input type="text" name="email" className="form-control" placeholder="ingrese el correo" onChange={handleChange} />
							<input type="text" name="name" className="form-control" placeholder="ingrese el nombre" onChange={handleChange} />
							<input type="password" name="password" className="form-control" placeholder="ingrese la contraseña" onChange={handleChange} />

							<button type="button" onClick={() => saveUser()} className="btn btn-success">Guardar usuario</button>
						</div>
					</form>
				</div>
			</div>
		</div>

	);
};
