import s from './LoginPage.module.scss';

export const LoginPage = () => {
  return (
    <div className={s.page}>
        <label>Логин</label>
        <input type="text" placeholder='Логин'/>
        <label>Пароль</label>
        <input type="text" placeholder='Пароль'/>
        <button>Отправить</button>
    </div>
  )
}
