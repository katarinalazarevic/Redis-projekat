import  './register.css'
const  Register = () =>
{
    return (
<div id="algn">
        <div id="container">
          <p className="head">Login</p>
          <form action="/" className="input-container">
            <input type="email" placeholder="Enter email" className="inpt" required />
            <input type="password" placeholder="Enter password" className="inpt" required />
            <div className="rem-forgot">
              <div className="rem">
                <input type="checkbox" id="rem-tik" />
                <label htmlFor="rem-tik">Remember me</label>
              </div>
              <span><a href="#">Forgot password</a></span>
            </div>
            <button type="submit" className="btn">Login</button>
          </form>
          <p className="footer">Don't have account nerd? <a href="#">Register</a></p>
        </div>
      </div>
    );

}

export default Register;