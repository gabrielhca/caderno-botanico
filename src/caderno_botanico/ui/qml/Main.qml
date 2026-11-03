pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: janela

    // Recebido do Python (ver app.py): o controlador que liga a tela ao Service.
    required property var controller

    // -1 = criando um caderno novo; qualquer outro valor = id do caderno em edição.
    property int cadernoEmEdicao: -1

    function limparFormulario() {
        cadernoEmEdicao = -1;
        campoNome.text = "";
        campoDescricao.text = "";
        mensagemErro.text = "";
    }

    function salvar() {
        mensagemErro.text = "";
        if (cadernoEmEdicao < 0)
            controller.criar(campoNome.text, campoDescricao.text);
        else
            controller.editar(cadernoEmEdicao, campoNome.text, campoDescricao.text);
    }

    width: 520
    height: 680
    visible: true
    title: qsTr("Caderno Botânico")

    Connections {
        function onCadernoSalvo() {
            janela.limparFormulario();
        }

        function onErroOcorrido(mensagem) {
            mensagemErro.text = mensagem;
        }

        target: janela.controller
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12

        Label {
            text: qsTr("Meus cadernos (%1)").arg(janela.controller.total)
            font.bold: true
            font.pixelSize: 20
        }

        Label {
            visible: janela.controller.total === 0
            text: qsTr("Nenhum caderno ainda. Crie o primeiro abaixo.")
            color: "gray"
        }

        ListView {
            id: lista

            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            model: janela.controller.cadernos

            delegate: ItemDelegate {
                required property int cadernoId
                required property string nome
                required property string descricao
                required property string criadoEm

                width: ListView.view.width
                text: nome + (descricao !== "" ? "\n" + descricao : "") + "\n" + qsTr("Criado em %1").arg(criadoEm)
                onClicked: {
                    janela.cadernoEmEdicao = cadernoId;
                    campoNome.text = nome;
                    campoDescricao.text = descricao;
                    mensagemErro.text = "";
                }
            }
        }

        Label {
            text: janela.cadernoEmEdicao < 0 ? qsTr("Novo caderno") : qsTr("Editando caderno")
            font.bold: true
        }

        TextField {
            id: campoNome

            objectName: "campoNome"
            Layout.fillWidth: true
            placeholderText: qsTr("Nome do caderno")
        }

        TextField {
            id: campoDescricao

            objectName: "campoDescricao"
            Layout.fillWidth: true
            placeholderText: qsTr("Descrição (opcional)")
        }

        Label {
            id: mensagemErro

            objectName: "mensagemErro"
            Layout.fillWidth: true
            color: "firebrick"
            wrapMode: Text.WordWrap
        }

        RowLayout {
            Layout.fillWidth: true

            Button {
                objectName: "botaoSalvar"
                text: janela.cadernoEmEdicao < 0 ? qsTr("Criar caderno") : qsTr("Salvar alterações")
                onClicked: janela.salvar()
            }

            Button {
                objectName: "botaoCancelar"
                text: qsTr("Cancelar")
                onClicked: janela.limparFormulario()
            }
        }
    }
}
