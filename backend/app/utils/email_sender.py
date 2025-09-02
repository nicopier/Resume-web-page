# email_sender.py
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
import smtplib
import ssl
from typing import Iterable, Union, Optional, List

class EmailSender:

    def __init__(
        self,
        gmail_user: str,
        app_password: str,
        from_name: Optional[str] = None,
        host: str = "smtp.gmail.com",
        port: int = 465,
        use_ssl: bool = True,
        timeout: int = 30,
    ) -> None:
        self.gmail_user = gmail_user
        self.app_password = app_password
        self.from_name = from_name
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.timeout = timeout

    def _normalize_recipients(self, r: Union[str, Iterable[str]]) -> List[str]:
        if isinstance(r, str):
            return [r]
        return [x for x in r if x]

    def send_html(
        self,
        to: Union[str, Iterable[str]],
        subject: str,
        html: str,
        cc: Optional[Union[str, Iterable[str]]] = None,
        bcc: Optional[Union[str, Iterable[str]]] = None,
        reply_to: Optional[str] = None,
        
    ) -> None:
        # Construir mensaje
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = formataddr((self.from_name or self.gmail_user, self.gmail_user))

        to_list  = self._normalize_recipients(to)
        cc_list  = self._normalize_recipients(cc)  if cc  else []
        bcc_list = self._normalize_recipients(bcc) if bcc else []

        if to_list:  msg["To"]  = ", ".join(to_list)
        if cc_list:  msg["Cc"]  = ", ".join(cc_list)
        if reply_to: msg["Reply-To"] = reply_to

        # Parte HTML (y un fallback de texto simple mínimo por compatibilidad)
        msg.set_content("Este mensaje está en formato HTML. Si ves este texto, usa un cliente compatible.")
        msg.add_alternative(html, subtype="html")

        # ID de contenido para imágenes inline si las usás luego (no obligatorio)
        msg["Message-ID"] = make_msgid()

        # Envío
        context = ssl.create_default_context()
        try:
            if self.use_ssl:
                with smtplib.SMTP_SSL(self.host, self.port, context=context, timeout=self.timeout) as s:
                    s.login(self.gmail_user, self.app_password)
                    s.send_message(msg, to_addrs=to_list + cc_list + bcc_list)
            else:
                with smtplib.SMTP(self.host, self.port, timeout=self.timeout) as s:
                    s.starttls(context=context)
                    s.login(self.gmail_user, self.app_password)
                    s.send_message(msg, to_addrs=to_list + cc_list + bcc_list)
        except smtplib.SMTPAuthenticationError as e:
            raise RuntimeError(
                "Fallo de autenticación SMTP. Verificá el Gmail y el App Password (2FA habilitado)."
            ) from e
        except Exception as e:
            # Re-lanzamos con un mensaje claro
            raise RuntimeError(f"Error enviando email: {e}") from e


#from email_sender import EmailSender

if __name__ == "__main__":
    sender = EmailSender(
        gmail_user="eldkchatarrero@gmail.com",
        app_password="busi wkmk ywdb mevf",   # generado en tu Gmail con 2FA
        from_name="resumeinterctivo"
    )

    sender.send_html(
        to="piersanti.nicolas@gmail.com",
        subject="Prueba de Email",
        html="<h1>Hola!</h1><p>Este es un correo de prueba en <b>HTML</b>.</p>"
    )

    print("✅ Email enviado")